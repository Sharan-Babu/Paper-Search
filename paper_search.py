import streamlit as st
from elasticsearch_dsl import connections, Search
from elasticsearch import Elasticsearch

st.set_page_config(page_title="Paper Search",page_icon="📄")
st.title("Paper Search  🕵")

st.sidebar.title("Similar Paper Finder 📃")

page = st.sidebar.radio("Select Page:",("Search Paper","Add Paper","Visualize available Papers"))


# Similarity search
def search(query, limit, column):
	query = {"size": limit,"query": {"query_string": {"query": query}}}
	results = []
	for result in client.search(index="knowledge_base", body=query)["hits"]["hits"]:
		source = result["_source"]
		#results.append((min(result["_score"], 18) / 18, source[column]))
		results.append((result["_score"], source[column], source['link']))
	return results	


try:
	with st.spinner("Connecting to ElasticSearch"):
		client = Elasticsearch(['https://enterprise-search-deployment-e1a20d.es.eastus2.azure.elastic-cloud.com:9243'], http_auth = ("elastic","qZoBF1Wm9nD3A8ZInkz0E630"))
except:
	st.info("ElasticSearch Instance not available. Try later")


if page == "Search Paper":
	st.title("Search Similar Papers 📑")
	
	st.caption('Example Title: 1D Convolutional Neural Networks Applications, Image captioning')

	column1 = st.selectbox("Select Filter Option:",("Title","abstract"))
	
	if column1 == "Title":
		user_input = st.text_input("Enter Title/Keywords of Paper:",'')
	elif column1 == "abstract":
		user_input = st.text_area("Enter Paper Abstract:",'',height=150)	
	

	if st.button('Find'):
		if user_input == '':
			st.warning("Please fill all fields.")
		else:	
			with st.spinner('Fetching Results...'):
				output = search(query=user_input,limit=10,column=column1)
				st.markdown('<h2><b>Top Results:',unsafe_allow_html=True)
				st.caption("Ranked based on Similarity")
				i = 1
				if len(output)==0:
					st.warning("No match. Add paper or try another keyword)
				for paper in output:
					st.markdown(f'{i}. {paper[1]}. <a href="{paper[2]}">Link</a>',unsafe_allow_html=True)
					i += 1
				st.balloons()		


elif page == "Add Paper":
	st.title('Add new paper to database 📖')
	st.caption('Sample data filled below.')

	# S.no
	# Label
	label = st.text_input("Enter Label/Category:","NLP")
	title = st.text_input("Enter Paper Title:","New NLP Paper")
	abstract = st.text_area("Enter Abstract:","This new Paper gives state of the art accuracy in ...",height=150)
	link = st.text_input("Paper Link","https://newnlp.com")

	data = {"Label":label,"Title":title,"abstract":abstract,"link":link}

	if st.button("Add Paper"):
		try:
			with st.spinner("Adding new data..."):
				res = client.index(index='knowledge_base',body=data)
				st.success("Paper Added Successfully")
		except:
			st.warning("Ensure valid details in all fields. Try again")	


elif page == "Visualize available Papers":
	st.title("Analysis 📊")
	st.markdown("""<a href="https://enterprise-search-deployment-e1a20d.kb.eastus2.azure.elastic-cloud.com:9243/app/dashboards#/view/a32376f0-bb6a-11eb-adae-81ceaf0c6ba0?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))">Interactive Dashboard Link</a>""",unsafe_allow_html=True)
	st.caption("Report Images")
	st.image('donut.PNG',width=440)
	st.image('bar_chart.PNG')
	

