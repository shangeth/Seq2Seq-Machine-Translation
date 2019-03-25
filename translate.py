from data_process import *
from model import *

MAX_LENGTH = 25
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
input_lang, output_lang, pairs = prepareData('eng', 'fra')


def evaluate(encoder, decoder, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = tensorFromSentence(input_lang, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)
        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS
        decoder_hidden = encoder_hidden
        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])
            decoder_input = topi.squeeze().detach()
        return decoded_words, decoder_attentions[:di + 1]

def evaluateAndShowAttention(input_sentence):
	#load model
	encoder1, attn_decoder1 = load_model()
    output_words, attentions = evaluate(
        encoder1, attn_decoder1, input_sentence)
    print('input =', input_sentence)
    print('output =', ' '.join(output_words))

def load_model():
	hidden_size = 256
	e = EncoderRNN(input_lang.n_words, hidden_size).to(device)
	d = AttnDecoderRNN(hidden_size, output_lang.n_words, dropout_p=0.1).to(device)
	checkpoint = torch.load(PATH)
	e.load_state_dict(checkpoint['encoder'])
	d.load_state_dict(checkpoint['decoder'])
	return e, d



def main(sentence):
	sentence = process_sentence(sentence)
	evaluateAndShowAttention(sentence)
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
    parser.add_argument("--translate_sentence", help="sentence to translate", default=True)
    args = parser.parse_args()
    main(args.translate_sentence)
 
