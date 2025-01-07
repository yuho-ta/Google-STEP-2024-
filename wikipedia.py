import sys
import collections
from collections import deque
class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file,'r',encoding="utf-8") as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file,'r',encoding="utf-8") as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    
    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def get_keys_from_value(self, d, val):    #単語に対応するidを返す
        for k, v in d.items():
            if v == val:
                return k
        return None
       
    def find_path(self, parent_node, depth, node):   
        path = [self.titles[node]]
        while depth != 0:
            node = parent_node[node]
            path.append(self.titles[node])
            depth -= 1
        path.reverse()
        return path

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal): 
        start_id =self.get_keys_from_value(self.titles,start)
        goal_id = self.get_keys_from_value(self.titles,goal)

        if start_id == None or goal_id == None:   #もしidが見つからなければ返す
            return "targets are not in wikipedia"
        elif start_id == goal_id: #スタートとゴールが同じだったらstartを返す
            return start
        
        d = deque()
        visited = {}
        visited[start_id] = True
        d.append(start_id)
        depth = [0] * (max(self.links.keys()) + 1)   #探索の深さを記録
        parent_node = [None] * (max(self.links.keys()) + 1) #親ノードのidを記録

        while d:
            node = d.popleft()
            if node == goal_id:
                return self.find_path(parent_node, depth[node], node)   #parent_nodeを用いて経路を復元
                
            for child in self.links[node]:
                if not child in visited:
                    visited[child] = True
                    d.append(child)
                    depth[child] = depth[node] + 1  #親ノードの深さを1つ足したものを代入
                    parent_node[child] = node #親ノードを代入
            
        return "there is no path"
        

    def is_not_stable(self, page_ranks, new_page_ranks, threshold):  
        for page_id in page_ranks.keys():
            if abs(page_ranks[page_id] - new_page_ranks[page_id]) >= threshold:
                return True
        return False

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        page_ranks = {page_id: 1 for page_id in self.titles.keys()}
        new_page_ranks = {page_id: 0 for page_id in self.titles.keys()}

        

        while self.is_not_stable(page_ranks, new_page_ranks,  1): #収束判定
            new_page_ranks = {page_id: 0 for page_id in self.titles.keys()}
            all_have_rank = 0  #全てのノードに足すランク

            for page_id in page_ranks.keys():
                if self.links[page_id]: #もしエッジを持っていたら
                    for linked_page_id in self.links[page_id]:
                        new_page_ranks[linked_page_id] += ( page_ranks[page_id] * 0.85 ) / len(self.links[page_id])
                    all_have_rank += page_ranks[page_id] * 0.15 / len(page_ranks)

                else:
                    all_have_rank += page_ranks[page_id] / len(page_ranks)
                
            for page_id in new_page_ranks.keys():  #全てのノードにall_have_rankを足す
                new_page_ranks[page_id] += all_have_rank

            page_ranks = new_page_ranks.copy() #page_ranksの更新
       
        sorted_pages = sorted(page_ranks.items(), key=lambda x: x[1], reverse=True) #ランクの値でソート
        top_pages = [self.titles[page_id] for page_id, _ in sorted_pages[:10]]
        return top_pages

        

    # Do something more interesting!!
    def suggestion_function(self, search):  
        '''
        課題1と2を合わせたおすすめ機能
        ノードごとのページランクを格納した辞書を作り、指定された文字からBFSを行って
        深さ2以内にあるランクが高い単語10個を返す
        '''
        page_ranks = {page_id: 1 for page_id in self.titles.keys()}
        new_page_ranks = {page_id: 0 for page_id in self.titles.keys()}

        while self.is_not_stable(page_ranks, new_page_ranks,  1): #収束判定
            new_page_ranks = {page_id: 0 for page_id in self.titles.keys()}
            all_have_rank = 0  #全てのノードに足すランク

            for page_id in page_ranks.keys():
                if self.links[page_id]: #もしエッジを持っていたら
                    for linked_page_id in self.links[page_id]:
                        new_page_ranks[linked_page_id] += ( page_ranks[page_id] * 0.85 ) / len(self.links[page_id])
                    all_have_rank += page_ranks[page_id] * 0.15 / len(page_ranks)

                else:
                    all_have_rank += page_ranks[page_id] / len(page_ranks)
                
            for page_id in new_page_ranks.keys():  #全てのノードにall_have_rankを足す
                new_page_ranks[page_id] += all_have_rank

            page_ranks = new_page_ranks.copy() #page_ranksの更新
        
        search_id =self.get_keys_from_value(self.titles,search)
       
        if search_id == None:   #もしidが見つからなければ返す
            return "target is not in wikipedia"
        
        d = deque()
        visited = {}
        visited[search_id] = True
        d.append(search_id)
        must_be_interesting = [] #おすすめ単語を保持
        max_depth = 2  #探索範囲の最大値
        depth = [0] * (max(self.links.keys()) + 1)
        while d:
            node = d.popleft()
            if not self.titles[node].endswith("年"):  #年はランクが高いが抽象的すぎるのでパス

                if len(must_be_interesting) < 10: #格納要素が10個より少なかったら
                    must_be_interesting.append((node, page_ranks[node]))
                    must_be_interesting.sort(key=lambda x: x[1], reverse=True)

                elif page_ranks[node] > must_be_interesting[-1][1]: #格納要素が10個より多かったら
                    must_be_interesting[-1] = (node, page_ranks[node])
                    must_be_interesting.sort(key=lambda x: x[1], reverse=True)

            for child in self.links[node]:
                if not child in visited:
                    visited[child] = True
                    d.append(child)
                    depth[child] = depth[node] + 1
                    if depth[child] > max_depth: #深さが最大の探索範囲を超えたら返す
                        return [(self.titles[page_id], rank) for page_id, rank in must_be_interesting]
        return [(self.titles[page_id], rank) for page_id, rank in must_be_interesting] #最大の探索範囲に到達する前にキューが空になったら返す
            

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    #wikipedia.find_longest_titles()
    #wikipedia.find_most_linked_pages()
    #print(wikipedia.find_shortest_path("渋谷", "パレートの法則"))
    #print(wikipedia.find_shortest_path("A", "E"))
    #print(wikipedia.find_most_popular_pages())
    print(wikipedia.suggestion_function("地球は女で回ってる"))
