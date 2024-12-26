import time

class KeywordYake:
    def __init__(self, text, language="en", max_ngram_size=3, deduplication_threshold=0.9, deduplication_algo='seqm', windowSize=1, numOfKeywords=5):
        import yake
        self.text = text
        self.language = language
        self.max_ngram_size = max_ngram_size
        self.deduplication_threshold = deduplication_threshold
        self.deduplication_algo = deduplication_algo
        self.windowSize = windowSize
        self.numOfKeywords = numOfKeywords
        self.custom_kw_extractor = yake.KeywordExtractor(
            lan=self.language, 
            n=self.max_ngram_size, 
            dedupLim=self.deduplication_threshold, 
            dedupFunc=self.deduplication_algo, 
            windowsSize=self.windowSize, 
            top=self.numOfKeywords, 
            features=None
        )

    def extract_keywords(self):
        time_start = time.time()
        keywords = self.custom_kw_extractor.extract_keywords(self.text)
        print(f'Time taken: {time.time() - time_start} seconds')
        return keywords
    

class KeywordBert:
    def __init__(self, text):
        from keybert import KeyBERT
        self.text = text
        self.model = KeyBERT()

    def extract_keywords(self):
        time_start = time.time()
        result =  self.model.extract_keywords(self.text)
        print(f'Time taken: {time.time() - time_start} seconds')
        return result


class KeywordPKE:
    def __init__(self, text, language="en", n_best=10):
        import pke
        
        self.text = text
        self.language = language
        self.n_best = n_best
        self.extractor = pke.unsupervised.TopicRank()
        
    def extract_keywords(self):
        start = time.time()
        
        # load document and preprocess using spacy
        self.extractor.load_document(input=self.text, language=self.language)
        
        # select candidates - sequences of nouns and adjectives
        self.extractor.candidate_selection()
        
        # weight candidates using random walk algorithm
        self.extractor.candidate_weighting()
        
        # get n-best keyphrases as (keyphrase, score) tuples
        keyphrases = self.extractor.get_n_best(n=self.n_best)
        
        print(f'Time taken: {time.time() - start} seconds')
        return keyphrases

doc = """
         Sarah, visiting from sunny Miami, Florida, met with Dr. Chen at the bustling Grand Central Terminal in New York City. They discussed the upcoming conference in London, England, focusing on the works of Shakespeare and the historical significance of the Tower of London. A nearby street performer, dressed as a convincing Abraham Lincoln, played a mournful tune on his saxophone, drawing a small crowd. The scent of hot dogs from a vendor cart mingled with the faint aroma of "old books" (a misleading marketing campaign for a new perfume). The conversation briefly touched on the recent archaeological discoveries in Petra, Jordan, before Sarah mentioned her upcoming trip to visit her grandmother in Des Moines, Iowa, for the annual "Corn Festival" (a local event known for its surprisingly good chili). Someone overheard them talking about the "London Bridge" (which is actually in Lake Havasu City, Arizona), adding to the general confusion of the location.
      """

def benchmark(doc):
    # Create instances of each keyword extractor
    yake_extractor = KeywordYake(doc)
    bert_extractor = KeywordBert(doc)
    pke_extractor = KeywordPKE(doc)

    # Extract keywords using each method
    print("\nYAKE keywords:")
    yake_results = yake_extractor.extract_keywords()
    print(yake_results)

    print("\nKeyBERT keywords:")
    bert_results = bert_extractor.extract_keywords()
    print(bert_results)

    print("\nPKE keywords:")
    pke_results = pke_extractor.extract_keywords()
    print(pke_results)

    return {
        'yake': yake_results,
        'keybert': bert_results,
        'pke': pke_results
    }
