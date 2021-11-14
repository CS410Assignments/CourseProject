#adapted from data_cleaning.ipynb
import gzip
import json


if __name__=="__main__":
    
    input_filename="goodreads_books.json.gz"
    output_filename="goodreads_books_cleaned2.json.gz"


    c=0

    popular_shelves = {}
    author_roles = {}
    with gzip.GzipFile(input_filename, 'r',) as fin:
        with gzip.open(output_filename, 'w') as f:
            data_lan = []
            while c < 2360000:
                #for line in fin:
                line = fin.readline()
                c+=1
                if c%1000==0:
                    print(c)
                info=json.loads(line.decode('utf-8'))
                try:
                    if ((info['language_code']=='eng') |(info['country_code'] == 'US') ):
                        #print(info)
                        new_info={}
                        new_info['title']=info['title']
                        new_info['book_id']=info['book_id']
                        new_info['authors']=info['authors']
                        new_info['series'] = info['series']
                        new_info['similar_books']=info['similar_books']
                        new_info['popular_shelves'] = info['popular_shelves']
                        new_info['description'] = info['description'].lower().replace(',','')
                        new_info['publication_year'] = info['publication_year']
                        new_info['rating']=info['average_rating']
                        new_info['ratings_count']=info['average_rating']
                        new_info['text_reviews_count']=info['text_reviews_count']
                        new_info['num_pages'] = info['num_pages']
                        #print((json.dumps(new_info)+'\n').encode('utf-8'))
                        #data_lan.append(new_info)

                        f.write((json.dumps(new_info)+'\n').encode('utf-8'))
                        if(new_info['authors']):
                            for author_item in new_info['authors']:
                                if author_item['role'] in author_roles:
                                    #print('role %s exists!'%author_item['role'])
                                    author_roles[author_item['role']] += 1
                                else:
                                    #print('role %s added!'%author_item['role'])
                                    author_roles[author_item['role']] = 1
                        if(new_info['popular_shelves']):
                            for shelf_item in new_info['popular_shelves']:
                                if shelf_item['name'] in popular_shelves:
                                    #print('shelf %s exists!'%shelf_item['name'])
                                    popular_shelves[shelf_item['name']] += 1
                                else:
                                    #print('shelf %s added!'%shelf_item['name'])
                                    popular_shelves[shelf_item['name']] = 1
                except:
                    pass
                

    print(author_roles)
    print(popular_shelves)

    with open('author_roles.txt', 'w') as f:
        for role in author_roles:
            f.write(role)
            f.write('/n')    

    with open('popular_shelves.txt', 'w') as f:
        for shelf in popular_shelves:
            f.write(shelf)
            f.write('/n')

    #with gzip.open(output_filename, 'w') as f:
    #    content=[]
    #    for dict in data_lan:
    #        content.append((json.dumps(dict)+'\n').encode('utf-8'))
    #    f.writelines(content)