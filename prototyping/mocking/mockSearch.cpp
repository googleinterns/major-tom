#include <bits/stdc++.h>
using namespace std;

// search function
// input: array of article text
// input: set of words to search through
// return: frequency map of articles and amount of incidences between 
// 	   words from the text and words in the set
// debugging output: every match between a word from an article and a
// 		     word from the set is printed
unordered_map<string, int> search(unordered_set<string> words, vector<string> articles) {
	unordered_map<string, int> incidences;

	for (const auto & article : articles) {
		string curr_word = "";
		
		for (const auto & letter : article) {
			if (!isalpha(letter)) {
				if (words.find(curr_word) != words.end()) {
					cout << curr_word << "\n";
					incidences[article]++;
				}

				curr_word = "";
			} else {
				curr_word += letter;
			}
		}
		if (words.find(curr_word) != words.end()) {
			incidences[article]++;
		}
	}
	return incidences;
} 

int main() {
	vector<string> articles{"Los conductores y ocupantes de bicicletas, bicimotos o triciclos podran utilizar de preferencia casco de proteccion para su seguridad.",
	       	"La autoridad municipal podra determinar la instalación de relojes estacionometros en la via publica, previo estudio de factibilidad elaborado por la Secretaria.",
		"No se autorizara ningun exclusivo para taxis a una distancia menor de 300-trescientos metros a la redonda de otro sitio de taxis autorizados.",
		"Las calcomania del refrendo del vehiculo deberan colocarse en el espacio establecido en la placa de circulacion."};

	unordered_set<string> keywords_article_1 = {"obligatorio", "utilizar", "casco"}; // Es obligatorio el uso de casco
	unordered_set<string> keywords_article_2 = {"via", "publica", "relojes"}; // Hay relojes en la via publica
	unordered_set<string> keywords_article_3 = {"taxis", "exclusivo", "autorizados", "radio"}; // taxis exclusivo autorizados radio
	unordered_set<string> keywords_article_4 = {"calcomania", "placa"}; // se cayo mi placa calcomania
	vector<unordered_set<string>> queries { keywords_article_1, keywords_article_2, keywords_article_3, keywords_article_4 };
	
	for (int i = 0; i < queries.size(); i++) {
		cout << "Query #" << i + 1 << ":\n";
		unordered_map<string, int> incidences = search(queries[i], articles);
		
		// Prints all articles which had a match for the specific query
		for (auto it = incidences.begin(); it != incidences.end(); it++) {
			cout << "\t" << it->first << "\n\tcount: " << it->second << "\n\n";
		}
	}
}
