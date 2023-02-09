from general_functions import open_web
from web_scraping import (
    webster,
    britannica,
    dictionary,
    bitesize,
    wikipedia,
    sparknotes, 
    booksummary,
    history,
    reuters,
    scholar
)
from frequency_analysis import list_to_summary
from database import (
    create_tables,
    output_saved_to_table,
    SourceSave,
    Record,
    make_save,
    remove_record,
    load_save,
    reset_tables
)
import PySimpleGUI as sg

def main():
    """Function: main
     @ 
    Main function of the 'Fountain of Knowledge' program
    """
    sg.theme("SystemDefaultForReal")
    width = 1000
    height = 700
    tabsize = (1920, 1080)

    #creation of the source table
    create_tables()
    save_headings = ["Saved Query"]
    saved_searches_table = [sg.Table(values = output_saved_to_table(), key= "save_values", headings = save_headings, size = tabsize, display_row_numbers = True, justification = "center", expand_x = True, alternating_row_color = "lightgray", selected_row_colors = "gray", enable_events=True, num_rows=256, auto_size_columns = True, hide_vertical_scroll = True)]

    #tab layouts
    bar_length = 210
    link_button_size = (6,2)
    summary_text_size = (115, 3)
    basic = [
        [sg.Button("Link", size=link_button_size, key="webster_link", enable_events = True), sg.Text("Merriam-Webster", key = "webster_title")], [sg.Text("", key = "webster_text", size = summary_text_size)], 
        [sg.Text("_" * bar_length)], 
        [sg.Button("Link", size=link_button_size, key= "britannica_link", enable_events = True), sg.Text("Britannica", key= "britannica_title")], [sg.Text("", key="britannica_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)], 
        [sg.Button("Link", size=link_button_size, key="dictionary_link", enable_events = True), sg.Text("Dictionary.com", key = "dictionary_title")], [sg.Text("", key = "dictionary_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "bitesize_link", enable_events = True), sg.Text("BBC Bitesize", key= "bitesize_title")], [sg.Text("", key= "bitesize_text", size = summary_text_size)]
        ]
    intermediate = [
        [sg.Button("Link", size=link_button_size, key= "wiki_link", enable_events = True), sg.Text("Wikipedia", key= "wiki_title")], [sg.Text("", key="wiki_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "spark_link", enable_events = True), sg.Text("SparkNotes", key= "spark_title")], [sg.Text("", key= "spark_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "booksummary_link", enable_events = True), sg.Text("BookSummary.net", key= "booksummary_title")], [sg.Text("", key= "booksummary_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "history_link", enable_events = True), sg.Text("History.com", key= "history_title")], [sg.Text("", key= "history_text", size = summary_text_size)]
        ]
    articles = [
        [sg.Button("Link", size=link_button_size, key= "reuters1_link", enable_events = True), sg.Text("Reuters 1", key= "reuters1_title")], [sg.Text("", key="reuters1_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "reuters2_link", enable_events = True), sg.Text("Reuters 2", key= "reuters2_title")], [sg.Text("", key="reuters2_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "reuters3_link", enable_events = True), sg.Text("Reuters 3", key= "reuters3_title")], [sg.Text("", key="reuters3_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "reuters4_link", enable_events = True), sg.Text("Reuters 4", key= "reuters4_title")], [sg.Text("", key="reuters4_text", size = summary_text_size)]
        ]
    academic = [
        [sg.Button("Link", size=link_button_size, key= "scholar1_link", enable_events = True), sg.Text("Google Scholar 1", key= "scholar1_title")], [sg.Text("", key="scholar1_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "scholar2_link", enable_events = True), sg.Text("Google Scholar 2", key= "scholar2_title")], [sg.Text("", key="scholar2_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "scholar3_link", enable_events = True), sg.Text("Google Scholar 3", key= "scholar3_title")], [sg.Text("", key="scholar3_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "scholar4_link", enable_events = True), sg.Text("Google Scholar 4", key= "scholar4_title")], [sg.Text("", key="scholar4_text", size = summary_text_size)],
        [sg.Text("_" * bar_length)],
        [sg.Button("Link", size=link_button_size, key= "further1_link", enable_events = True), sg.Text("Further Reading 1", key= "further1_title")],
        [sg.Button("Link", size=link_button_size, key= "further2_link", enable_events = True), sg.Text("Further Reading 2", key= "further2_title")],
        [sg.Button("Link", size=link_button_size, key= "further3_link", enable_events = True), sg.Text("Further Reading 3", key= "further3_title")],
        [sg.Button("Link", size=link_button_size, key= "further4_link", enable_events = True), sg.Text("Further Reading 4", key= "further4_title")]
        ]
    saved = [
        [sg.Button("Delete Record"), sg.Button("Reset Table")],
        saved_searches_table
        ]

    layout_basic = [[sg.Column(basic, scrollable=True,  vertical_scroll_only=True, size = tabsize, expand_x = True, expand_y = True)]]
    layout_intermediate = [[sg.Column(intermediate, scrollable=True,  vertical_scroll_only=True, size = tabsize, expand_x = True, expand_y = True)]]
    layout_articles = [[sg.Column(articles, scrollable=True,  vertical_scroll_only=True, size = tabsize, expand_x = True, expand_y = True)]]
    layout_academic = [[sg.Column(academic, scrollable=True,  vertical_scroll_only=True, size = tabsize, expand_x = True, expand_y = True)]]
    layout_savedsearches = [[sg.Column(saved, scrollable=True,  vertical_scroll_only=True, size = tabsize, expand_x = True, expand_y = True, element_justification = "c")]]

    tabs = sg.TabGroup([[sg.Tab("  Basic  ", layout_basic), 
                        sg.Tab("  Intermediate  ", layout_intermediate),
                        sg.Tab("  Articles  ", layout_articles), 
                        sg.Tab("  Academic  ", layout_academic),
                        sg.Tab("  Saved Searches  ", layout_savedsearches)]], tab_location = "top", size = tabsize)

    SearchScreenLayout = [
                        [sg.Text("Search:"), sg.InputText(size = (25,1), key = "iquery") , sg.Button("Enter"), sg.Button("Save"), sg.Button("Load"), sg.Text("", key= "progress_bar")], 
                        [tabs]
                        ]
    
    window = sg.Window("The Fountain of Knowledge", SearchScreenLayout, size = (width,height), resizable = True)
    
    def source_block(source_name: str, title: str, link: str, freqlist: str, title_key: str, text_key: str):
        """Function: source_block
        @params
        source_name: name of the source
        title: title of the source
        link: link to the source
        freq_list: frequency list of the source
        title_key: title key of the source block's title
        text_key: text key for the source block's main text

        Outputs a source to its block in the GUI.
        """
        window[title_key].update(value = str(source_name + ": " + title + " - " + link))
        window[text_key].update(value = (freqlist))
        return title, link, freqlist

    searched = False   
    while True:
        event, values = window.read()
        if event == "Enter":
            searched = True
            input_query = values["iquery"]

            #Basic
            webster_title, webster_link, webster_freqlist = webster(input_query)
            webster_summary = list_to_summary(webster_freqlist)
            webster_save = SourceSave("webster", webster_title, webster_link, webster_summary)
            source_block("Merriam-Webster", webster_title, webster_link, webster_summary, "webster_title", "webster_text")

            britannica_title, britannica_link, britannica_freqlist = britannica(input_query)
            britannica_summary = list_to_summary(britannica_freqlist)
            britannica_save = SourceSave("britannica", britannica_title, britannica_link, britannica_summary)
            source_block("Britannica", britannica_title, britannica_link, britannica_summary, "britannica_title", "britannica_text")

            dictionary_title, dictionary_link, dictionary_freqlist = dictionary(input_query)
            dictionary_summary = list_to_summary(dictionary_freqlist)
            dictionary_save = SourceSave("dictionary", dictionary_title, dictionary_link, dictionary_summary)
            source_block("Dictionary.com", dictionary_title, dictionary_link, dictionary_summary, "dictionary_title", "dictionary_text")

            bitesize_title, bitesize_link, bitesize_freqlist = bitesize(input_query)
            bitesize_summary = list_to_summary(bitesize_freqlist)
            bitesize_save = SourceSave("bitesize", bitesize_title, bitesize_link, bitesize_summary)
            source_block("BBC Bitesize", bitesize_title, bitesize_link, bitesize_summary, "bitesize_title", "bitesize_text")

            #Intermediate
            wiki_title, wiki_link, wiki_freqlist = wikipedia(input_query)
            wiki_summary = list_to_summary(wiki_freqlist)
            wiki_save = SourceSave("wikipedia", wiki_title, wiki_link, wiki_summary)
            source_block("Wikipedia", wiki_title, wiki_link, wiki_summary, "wiki_title", "wiki_text")

            spark_title, spark_link, spark_freqlist = sparknotes(input_query)
            spark_summary = list_to_summary(spark_freqlist)
            spark_save = SourceSave("sparknotes", spark_title, spark_link, spark_summary)
            source_block("SparkNotes", spark_title, spark_link, spark_summary, "spark_title", "spark_text")

            booksummary_title, booksummary_link, booksummary_freqlist = booksummary(input_query)
            booksummary_summary = list_to_summary(booksummary_freqlist)
            booksummary_save = SourceSave("booksummary", booksummary_title, booksummary_link, booksummary_summary)
            source_block("BookSummary.net", booksummary_title, booksummary_link, booksummary_summary, "booksummary_title", "booksummary_text")

            history_title, history_link, history_freqlist = history(input_query)
            history_summary = list_to_summary(history_freqlist)
            history_save = SourceSave("history", history_title, history_link, history_summary)
            source_block("History.com", history_title, history_link, history_summary, "history_title", "history_text")

            #Articles
            reuters_list = reuters(input_query)
            reuters_saves = []
            for index in range(0,4):
                i = index + 1
                website_name = "reuters" + str(i)
                reuters_save = SourceSave(website_name, reuters_list[index][0], reuters_list[index][1], list_to_summary(reuters_list[index][2]))
                reuters_saves.append(reuters_save)
                source_name = "Reuters " + str(i)
                title_key = "reuters" + str(i) + "_title"
                text_key = "reuters" + str(i) + "_text"
                source_block(source_name, reuters_list[index][0], reuters_list[index][1], list_to_summary(reuters_list[index][2]), title_key, text_key)

            #Academic / Further Reading
            scholar_list, further_list = scholar(input_query)
            scholar_saves = []
            further_saves = []
            for index in range(0, 4):
                i = index + 1
                website_name = "scholar" + str(i)
                scholar_save = SourceSave(website_name, scholar_list[index][0], scholar_list[index][1], list_to_summary(scholar_list[index][2]))
                scholar_saves.append(scholar_save)
                source_name = "Google Scholar " + str(i)
                title_key = "scholar" + str(i) + "_title"
                text_key = "scholar" + str(i) + "_text"
                source_block(source_name, scholar_list[index][0], scholar_list[index][1], list_to_summary(scholar_list[index][2]), title_key, text_key)

            for index in range(0,4):
                i = index + 1
                website_name = "further" + str(i)
                further_save = SourceSave(website_name, further_list[index][0], further_list[index][1], "No Summary Available")
                further_saves.append(further_save)
                source_name = "Further Reading " + str(i)
                title_key = "further" + str(i) + "_title"
                window[title_key].update(value = str(source_name + ": " + further_list[index][0] + " - " + further_list[index][1]))

        #Basic
        if event == "webster_link":
            try:
                open_web(webster_link)
            except:
                open_web("https://www.merriam-webster.com/dictionary/")
        if event == "britannica_link":
            try:
                open_web(britannica_link)
                pass
            except:
                open_web("https://www.britannica.com/")
        if event == "dictionary_link":
            try:
                open_web(dictionary_link)
                pass
            except:
                open_web("https://www.dictionary.com/")
        if event == "bitesize_link":
            try:
                open_web(bitesize_link)
            except:
                open_web("https://www.bbc.co.uk/bitesize/")
    
        #Intermediate
        if event == "wiki_link":
            try:
                open_web(wiki_link)
            except:
                open_web("https://en.wikipedia.org/wiki/")
        if event == "spark_link":
            try:
                open_web(spark_link)
            except:
                open_web("https://www.sparknotes.com/")
        if event == "booksummary_link":
            try:
                open_web(booksummary_link)
            except:
                open_web("https://www.booksummary.net/")
        if event == "history_link":
            try:
                open_web(history_link)
            except:
                open_web("https://www.history.co.uk/")
        
        #Articles
        if event == "reuters1_link":
            try:
                open_web(reuters_saves[0].l)
            except:
                open_web("https://www.reuters.com/search")
        if event == "reuters2_link":
            try:
                open_web(reuters_saves[1].l)
            except:
                open_web("https://www.reuters.com/search")
        if event == "reuters3_link":
            try:
                open_web(reuters_saves[2].l)
            except:
                open_web("https://www.reuters.com/search")
        if event == "reuters4_link":
            try:
                open_web(reuters_saves[3].l)
            except:
                open_web("https://www.reuters.com/search")

        #Academic
        if event == "scholar1_link":
            try:
                open_web(scholar_saves[0].l)
            except:
                open_web("https://scholar.google.com/")
        if event == "scholar2_link":
            try:
                open_web(scholar_saves[1].l)
            except:
                open_web("https://scholar.google.com/")
        if event == "scholar3_link":
            try:
                open_web(scholar_saves[2].l)
            except:
                open_web("https://scholar.google.com/")
        if event == "scholar4_link":
            try:
                open_web(scholar_saves[3].l)
            except:
                open_web("https://scholar.google.com/")

        #Further Reading
        if event == "further1_link":
            try:
                open_web(further_saves[0].l)
            except:
                open_web("https://scholar.google.com/")
        if event == "further2_link":
            try:
                open_web(further_saves[1].l)
            except:
                open_web("https://scholar.google.com/")
        if event == "further3_link":
            try:
                open_web(further_saves[2].l)
            except:
                open_web("https://scholar.google.com/")
        if event == "further4_link":
            try:
                open_web(further_saves[3].l)
            except:
                open_web("https://scholar.google.com/")
        
        if event == "Save" and searched == True:
            save = Record(webster_save, britannica_save, dictionary_save, bitesize_save, wiki_save, spark_save, booksummary_save, history_save, reuters_saves[0], reuters_saves[1], reuters_saves[2], reuters_saves[3], scholar_saves[0], scholar_saves[1], scholar_saves[2], scholar_saves[3], further_saves[0], further_saves[1], further_saves[2], further_saves[3])
            make_save(save, input_query)
            window["save_values"].update(values = (output_saved_to_table()))

        if event == "save_values":
            try:
                loadable = values["save_values"][0]
            except:
                loadable = 0

        if event == "Delete Record":
            remove_record(loadable)
            window["save_values"].update(values = (output_saved_to_table()))

        if event == "Load":
            try:
                loaded_save = load_save(loadable)
                table = loaded_save.tblSave

                webster_title, webster_link, webster_freqlist = source_block("Merriam-Webster", table[0][1], table[0][2], table[0][3], "webster_title", "webster_text")
                britannica_title, britannica_link, britannica_freqlist = source_block("Britannica", table[1][1], table[1][2], table[1][3], "britannica_title", "britannica_text")
                dictionary_title, dictionary_link, dictionary_freqlist = source_block("Dictionary.com", table[2][1], table[2][2], table[2][3], "dictionary_title", "dictionary_text")
                bitesize_title, bitesize_link, bitesize_freqlist = source_block("BBC Bitesize", table[3][1], table[3][2], table[3][3], "bitesize_title", "bitesize_text")
                
                wiki_title, wiki_link, wiki_freqlist = source_block("Wikipedia", table[4][1], table[4][2], table[4][3], "wiki_title", "wiki_text")
                spark_title, spark_link, spark_freqlist = source_block("SparkNotes", table[5][1], table[5][2], table[5][3], "spark_title", "spark_text")
                booksummary_title, booksummary_link, booksummary_freqlist = source_block("BookSummary.net", table[6][1], table[6][2], table[6][3], "booksummary_title", "booksummary_text")
                history_title, history_link, history_freqlist = source_block("History.com", table[7][1], table[7][2], table[7][3], "history_title", "history_text")

                reuters1_title, reuters1_link, reuters1_freqlist = source_block("Reuters 1", table[8][1], table[8][2], table[8][3], "reuters1_title", "reuters1_text")
                reuters2_title, reuters2_link, reuters2_freqlist = source_block("Reuters 2", table[9][1], table[9][2], table[9][3], "reuters2_title", "reuters2_text")
                reuters3_title, reuters3_link, reuters3_freqlist = source_block("Reuters 3", table[10][1], table[10][2], table[10][3], "reuters3_title", "reuters3_text")
                reuters4_title, reuters4_link, reuters4_freqlist = source_block("Reuters 4", table[11][1], table[11][2], table[11][3], "reuters4_title", "reuters4_text")
                reuters1 = SourceSave("reuters1", reuters1_title, reuters1_link, reuters1_freqlist)
                reuters2 = SourceSave("reuters2", reuters2_title, reuters2_link, reuters2_freqlist)
                reuters3 = SourceSave("reuters3", reuters3_title, reuters3_link, reuters3_freqlist)
                reuters4 = SourceSave("reuters4", reuters4_title, reuters4_link, reuters4_freqlist)
                reuters_saves = [reuters1, reuters2, reuters3, reuters4]

                scholar1_title, scholar1_link, scholar1_freqlist = source_block("Google Scholar 1", table[12][1], table[12][2], table[12][3], "scholar1_title", "scholar1_text")
                scholar2_title, scholar2_link, scholar2_freqlist = source_block("Google Scholar 2", table[13][1], table[13][2], table[13][3], "scholar2_title", "scholar2_text")
                scholar3_title, scholar3_link, scholar3_freqlist = source_block("Google Scholar 3", table[14][1], table[14][2], table[14][3], "scholar3_title", "scholar3_text")
                scholar4_title, scholar4_link, scholar4_freqlist = source_block("Google Scholar 4", table[15][1], table[15][2], table[15][3], "scholar4_title", "scholar4_text")
                scholar1 = SourceSave("scholar1", scholar1_title, scholar1_link, scholar1_freqlist)
                scholar2 = SourceSave("scholar2", scholar2_title, scholar2_link, scholar2_freqlist)
                scholar3 = SourceSave("scholar3", scholar3_title, scholar3_link, scholar3_freqlist)
                scholar4 = SourceSave("scholar4", scholar4_title, scholar4_link, scholar4_freqlist)
                scholar_saves = [scholar1, scholar2, scholar3, scholar4]
                
                window["further1_title"].update(value = str("Further Reading 1" + ": " + table[16][1] + " - " + table[16][2]))
                window["further2_title"].update(value = str("Further Reading 2" + ": " + table[17][1] + " - " + table[17][2]))
                window["further3_title"].update(value = str("Further Reading 3" + ": " + table[18][1] + " - " + table[18][2]))
                window["further4_title"].update(value = str("Further Reading 4" + ": " + table[19][1] + " - " + table[19][2]))
                further1 = SourceSave("further1", table[16][1], table[16][2], "No Summary Available")
                further2 = SourceSave("further2", table[17][1], table[17][2], "No Summary Available")
                further3 = SourceSave("further3", table[18][1], table[18][2], "No Summary Available")
                further4 = SourceSave("further4", table[19][1], table[19][2], "No Summary Available")
                further_saves = [further1, further2, further3, further4]
            except:
                pass

        if event == "Reset Table":
            reset_tables()
            window["save_values"].update(values = (output_saved_to_table()))

        if event == sg.WIN_CLOSED:
            window.close()
            break

if __name__ == "__main__":
    main()