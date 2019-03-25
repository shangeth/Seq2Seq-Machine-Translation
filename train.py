from data_process import *
from model import *
import time
import math

SOS_token = 0
EOS_token = 1
teacher_forcing_ratio = 0.5
MAX_LENGTH = 25
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
input_lang, output_lang, pairs = prepareData('eng', 'fra')

def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))

def indexesFromSentence(lang, sentence):
	'''convert a sentence to indexes in the corpus'''
	return [lang.word2index[word] for word in sentence.split(' ')]

def tensorFromSentence(lang, sentence):
	''' sentence to index list to torch tensor'''
	indexes = indexesFromSentence(lang, sentence)
	indexes.append(EOS_token)
	return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)

def tensorsFromPair(pair):
	''' get tensors for input and target language sentences'''
	input_tensor = tensorFromSentence(input_lang, pair[0])
	target_tensor = tensorFromSentence(output_lang, pair[1])
	return (input_tensor, target_tensor)

def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, max_length=MAX_LENGTH):
	encoder_hidden = encoder.initHidden()
	encoder_optimizer.zero_grad()
	decoder_optimizer.zero_grad()

	input_length = input_tensor.size(0)
	target_length = target_tensor.size(0)
	encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)
	loss = 0
	for ei in range(input_length):
	    encoder_output, encoder_hidden = encoder(
	        input_tensor[ei], encoder_hidden)
	    encoder_outputs[ei] = encoder_output[0, 0]

	decoder_input = torch.tensor([[SOS_token]], device=device)
	decoder_hidden = encoder_hidden
	use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False

	if use_teacher_forcing:
	    # Teacher forcing: Feed the target as the next input
	    for di in range(target_length):
	        decoder_output, decoder_hidden, decoder_attention = decoder(
	            decoder_input, decoder_hidden, encoder_outputs)
	        loss += criterion(decoder_output, target_tensor[di])
	        decoder_input = target_tensor[di]  # Teacher forcing
	else:
	    # Without teacher forcing: use its own predictions as the next input
	    for di in range(target_length):
	        decoder_output, decoder_hidden, decoder_attention = decoder(
	            decoder_input, decoder_hidden, encoder_outputs)
	        topv, topi = decoder_output.topk(1)
	        decoder_input = topi.squeeze().detach()  # detach from history as input

	        loss += criterion(decoder_output, target_tensor[di])
	        if decoder_input.item() == EOS_token:
	            break
	loss.backward()
	encoder_optimizer.step()
	decoder_optimizer.step()
	return loss.item() / target_length	


def trainIters(encoder, decoder, n_iters, pairs, print_every=1000, plot_every=100, learning_rate=0.01):
	start = time.time()
	plot_losses = []
	print_loss_total = 0  # Reset every print_every
	plot_loss_total = 0  # Reset every plot_every

	encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
	decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
	training_pairs = [tensorsFromPair(random.choice(pairs))
	                  for i in range(n_iters)]
	criterion = nn.NLLLoss()
	for iter in range(1, n_iters + 1):
	    training_pair = training_pairs[iter - 1]
	    input_tensor = training_pair[0]
	    target_tensor = training_pair[1]

	    loss = train(input_tensor, target_tensor, encoder,
	                 decoder, encoder_optimizer, decoder_optimizer, criterion)
	    print_loss_total += loss
	    plot_loss_total += loss

	    if iter % print_every == 0:
	        print_loss_avg = print_loss_total / print_every
	        print_loss_total = 0
	        print('%s (%d %d%%) %.4f' % (timeSince(start, iter / n_iters),
	                                     iter, iter / n_iters * 100, print_loss_avg))

	    if iter % plot_every == 0:
	        plot_loss_avg = plot_loss_total / plot_every
	        plot_losses.append(plot_loss_avg)
	        plot_loss_total = 0
    save_model(encoder, decoder)


def save_model(e, d):
	torch.save({'encoder':e.state_dict(), 'decoder':d.state_dict()}, './trained_mdoel/seq2seq.net')



def main():
	parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", help="no of epochs to train", default=75000)
    parser.add_argument("--lr", help="learning rate", default=0.001)
    args = parser.parse_args()

	hidden_size = 256
	encoder1 = EncoderRNN(input_lang.n_words, hidden_size).to(device)
	attn_decoder1 = AttnDecoderRNN(hidden_size, output_lang.n_words, dropout_p=0.1).to(device)
	trainIters(encoder1, attn_decoder1, int(args.epochs), pairs, print_every=5000, float(args.lr))





if __name__ == '__main__':
	main()