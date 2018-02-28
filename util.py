def parse_and_format_csv(csv_input):
	# parse configs
	csv_config_headers = next(csv_input)
	csv_config = next(csv_input)
	start_phrase = csv_config[0]
	target_phrases_raw = csv_config[1].split(',')
	target_phrases = [tp.lstrip() for tp in target_phrases_raw]
	skip_phrases_raw = csv_config[2].split(',')
	skip_phrases = [sp.lstrip() for sp in skip_phrases_raw]

	#parse reports
	reports = []
	csv_report_headers = next(csv_input)
	for report in csv_input:
		report_text = report[0]
		reports.append(report_text)
	return [start_phrase, target_phrases, skip_phrases, reports, [csv_config_headers, csv_config, csv_report_headers]]
