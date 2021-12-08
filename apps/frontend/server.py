from flask import Flask
from flask import render_template, request, jsonify
import json
import os
import requests
import base64
import sys
import re
from apps.backend.utils.facultydb import FacultyDB
from apps.backend.api.search import Search


app = Flask(__name__, template_folder='web/templates')
app.rootpath = "web/templates"
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'web/templates'))

'''environ = 'development'
dataconfig = json.loads(open("config.json", "r").read())
app.dataenv = dataconfig[environ]
app.rootpath = dataconfig[environ]["rootpath"]
app.datasetpath = dataconfig[environ]['datasetpath']
app.searchconfig = dataconfig[environ]['searchconfig']
index = metapy.index.make_inverted_index(app.searchconfig)
query = metapy.index.Document()
uni_list = json.loads(open(dataconfig[environ]["unispath"],'r').read())["unis"]
loc_list = json.loads(open(dataconfig[environ]["locspath"],'r').read())["locs"]
'''
faculty = FacultyDB()
unis = json.dumps(faculty.get_all_universities())
locs = json.dumps(faculty.get_all_locations())
depts = json.dumps(faculty.get_all_departments())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

def filtered_results(results,num_results,min_score,selected_uni_filters,selected_loc_filters):
    filtered_results = []
    universities = []
    states =[]
    countries = []
    res_cnt = 0
    # print (selected_uni_filters,selected_loc_filters)
    for res in results:
        university = index.metadata(res[0]).get('university')
        state = index.metadata(res[0]).get('state')
        country = index.metadata(res[0]).get('country') 
        if (res[1]>min_score) and (state in selected_loc_filters or country in selected_loc_filters) and (university in selected_uni_filters) :
            filtered_results.append(res)
            res_cnt += 1
            universities.append(university)
            states.append(state)
            countries.append(country)
            if res_cnt == num_results:
                break
    return filtered_results,universities,states,countries


@app.route('/search', methods=['POST'])
def search():
    data = json.loads(request.data.decode("utf-8"))
    querytext = data['query']
    num_results = data['num_results']

    search_obj = Search()
    search_result = search_obj.get_search_results(querytext, "Manipal", "Computer", "Sikkim")

    print(search_result)

    '''
    selected_loc_filters = data['selected_loc_filters']
    selected_uni_filters = data['selected_uni_filters']

    

    query = metapy.index.Document()
    query.content(querytext)
    min_score = 0.01

    # Dynamically load the ranker
    sys.path.append(app.rootpath + "/expertsearch")

    from ranker import load_ranker

    ranker = load_ranker(app.searchconfig)

    results = ranker.score(index, query, 100) 

    results,universities,states,countries = filtered_results(results,num_results,min_score,selected_uni_filters,selected_loc_filters)

    doc_names = [index.metadata(res[0]).get('doc_name') for res in results]
    depts = [index.metadata(res[0]).get('department') for res in results]
    fac_names = [index.metadata(res[0]).get('fac_name') for res in results]
    fac_urls = [index.metadata(res[0]).get('fac_url') for res in results]
   

    previews = _get_doc_previews(doc_names,querytext)
    emails = [index.metadata(res[0]).get('email') for res in results]


    docs = list(zip(doc_names, previews, emails,universities,depts,fac_names,fac_urls,states,countries))
    '''
    return jsonify({
        "docs": search_result
    })



@app.route("/admin/ranker/get")
def get_ranker():
    ranker_path = app.rootpath + "/expertsearch/ranker.py"
    ranker_contents = open(ranker_path, 'r').read()

    return jsonify({
        "ranker_contents": ranker_contents
    })

@app.route("/admin/ranker/set", methods=["POST"])
def set_ranker():
    data = json.loads(request.data.decode("utf-8"))
    projectId = data["projectId"]
    apiToken = data["apiToken"]

    ranker_url = "https://lab.textdata.org/api/v4/projects/" + projectId + "/repository/files/search_eval.py?ref=master&private_token=" + apiToken
    resp = requests.get(ranker_url)

    gitlab_resp = json.loads(resp.content)
    file_content = gitlab_resp["content"]
    ranker_path = app.rootpath + "/expertsearch/ranker.py"

    with open(ranker_path, 'wb') as f:
        f.write(base64.b64decode(file_content))
        f.close()

    return "200"

def _get_doc_previews(doc_names,querytext):
    return list(map(lambda d: _get_preview(d,querytext), doc_names))

def format_string(matchobj):
    
    return '<b>'+matchobj.group(0)+'</b>'

def _get_preview(doc_name,querytext):
    preview = ""
    num_lines = 0
    preview_length = 2
    fullpath = app.datasetpath + "/" + doc_name

    with open(fullpath, 'r') as fp:
        while num_lines < preview_length:
            line = fp.readline()
            found_phrase = False
            if not line:
                break
            formatted_line = str(line.lower())
            for w in querytext.lower().split():

                (sub_str,cnt) = re.subn(re.compile(r"\b{}\b".format(w)),format_string,formatted_line)

                if cnt>0:
                    formatted_line = sub_str
                    found_phrase = True 

            if found_phrase:
                preview += formatted_line

                num_lines += 1
        fp.close()
 
    short_preview = ''
    prev_i = 0
    start = 0
    words = preview.split()
    cnt = 0
    i=0
   
    while i<len(words):
        

        
        if '<b>' in words[i]:
            start = min(i-prev_i,5)
            
            if  i-start>0:
                short_preview += '...'
            short_preview += ' '.join(words[i-start:i+5])
            i+=5
            prev_i = i
            cnt +=1
        else:
            i+=1
        if cnt==3:
            break


    return short_preview



if __name__ == '__main__':
    # environ = os.environ.get("APP_ENV")
    '''environ = 'development'
    dataconfig = json.loads(open("config.json", "r").read())
    app.dataenv = dataconfig[environ]
    app.rootpath = dataconfig[environ]["rootpath"]
    app.datasetpath = dataconfig[environ]['datasetpath']
    app.searchconfig = dataconfig[environ]['searchconfig']'''

    app.run(debug=True,threaded=True,host='localhost',port=8095)
