import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData
import networkx as nx


modifiers = itemData.instantiateFromCSVtoitemData(
    "https://raw.githubusercontent.com/chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.tsv")

def markup_sentence(sentence, modifiers, targets, prune_inactive=True):
    markup = pyConText.ConTextMarkup()
    markup.setRawText(sentence.lower())
    markup.cleanText()
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")
    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    # apply modifiers to any targets within the modifiers scope
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    if prune_inactive:
        markup.dropInactiveModifiers()
    return markup

def clean_up_report(report, start_phrase):
	report = report.lower()
	# remove text prior to start_phrase
	if start_phrase:
		if report.find(start_phrase.lower()) != -1:
			report = report[report.index(start_phrase.lower()) + len(start_phrase) : len(report)].lstrip()
	# replace all colons with periods
	report = ('.').join(report.split(':'))
	# split the report into sentences
	report_sentences = report.split('.')
	return report_sentences

def evaluate_report(report_sentences, skip_phrases, target_phrases, target_phrases_item_data):
	# print("Post cleaning up we are left with: " + report)
	# remove sentences that start wiht skip_phrases
	num_present = 0
	num_absent = 0
	report_relevant_phrases = []
	for sentence in report_sentences:
		# check that target phrase in this sentence
		if len(sentence.lstrip()) > 0:
			target_phrase_found = False
			for target_phrase in target_phrases:
				if sentence.lower().find(target_phrase.lower()):
					target_phrase_found = True
					break
			if target_phrase_found:
				# check for skip phrases
				skip_phrase_found = False
				for skip_phrase in skip_phrases:
					if sentence.lower().find(skip_phrase.lower()) != -1:
						skip_phrase_found = True
				# if no skip phrase found, search NegEx
				if not skip_phrase_found:
					evaluation = 'present'
					markup_results = markup_sentence(sentence, modifiers, target_phrases_item_data)
					for edge in markup_results.edges():
						if edge[0].categoryString() == 'definite_negated_existence':
							evaluation = 'absent'
					if evaluation == 'absent':
						num_absent += 1
					else:
						num_present += 1
					report_relevant_phrases.append({'sentence': sentence, 'evaluation': evaluation})
	final_evaluation = 'absent' if num_present < num_absent else 'present'
	ambiguous = False
	if num_absent != 0 and num_present != 0:
		ambiguous = True
	return {'final_evaluation': final_evaluation, 'ambiguous': ambiguous, 'num_present': num_present, 'num_absent': num_absent, 'relevant sentences': report_relevant_phrases}

def get_target_phrases_item_data(target_phrases):
	# make an itemData of our custom target phrases
	target_phrases_item_data = itemData.itemData()
	for target_phrase in target_phrases:
		# create a contextItem from the target phrase
		contextItemTarget = itemData.contextItem([target_phrase, target_phrase, target_phrase, target_phrase])
		target_phrases_item_data.append(contextItemTarget)
	return target_phrases_item_data

def evaluate_reports(target_phrases, start_phrase, skip_phrases, reports):
	target_phrases_item_data = get_target_phrases_item_data(target_phrases)
	evaluations = []
	for report in reports:
		report_sentences_clean = clean_up_report(report, start_phrase)
		evaluation = evaluate_report(report_sentences_clean, skip_phrases, target_phrases, target_phrases_item_data) 
		evaluations.append(evaluation)
	return evaluations

if __name__ == '__main__':
	target_phrases = ['pulmonary embolism', 'pe']
	report1 = 'Check if there is a pulmonary embolism.START SKIP THIS there is a pulmonary embolism. There is no pulmonary embolism.'
	report2 = 'there is a pulmonary embolism.'
	report3 = 'there is a pe.'
	reports = [report1, report2, report3]
	start_phrase = 'start'
	skip_phrases = ['SKIP THIS']
	evaluations = evaluate_reports(target_phrases, start_phrase, skip_phrases, reports)
	for evaluation in evaluations:
		print(evaluation)
