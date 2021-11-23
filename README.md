# HumanityTech
NGOBot is a simple interactive chatbot which allows users to find NGOs based on 2 parameters : Location and areas of work or categories. The aim is to allow anyone to find NGOs in India in simple conversation rather than having to manually set filters. This makes it easier to find NGOs relevant to you for donations, collaborations, support etc much faster and smoother than solutions available online.
Some simple examples of actual conversation are :
- NGOs in UP. [only state]
- NGOs in Delhi, Meerut, Bangalore and Chennai.[multiple cities]
- NGOs in Bangalore, Karnataka.[city within state]
- NGOs working in mental health.[single field of work]
- NGOs working in education, vocational training, hunger and infrastructure.[multiple fields of work]
- NGOs in Karnataka and Chennai involved in women's rights. [State,city and field of work]
- NGOs in Chennai, Bangalore and Ranchi working to develop rural infrastructure, banks and finance. [multiple cities and areas of work].

The chatbot can parse these combinations in any order (also in a successive data entry flow - first location then categories). Data is fetched from a database which is regularly updated from some popular NGO websites wherein the same searching process is much more cumbersome. The chat interface is then populated with all the relevant NGOs (as dropdown accordions with all relevant NGO information such as website, contact numbers, areas of work, location etc to make contacting these NGOs directly much easier). This same workflow can be easily repeated by following suggestion chips at every step.

---
## Stack
1. Frontend : HTML page integrated with Dialogflow(served as a page widget and integrated via a webhook with a single server for both the back and front end).
2. Backend : Flask (Python)
3. Database : MySQL
4. Frameworks : 
- Dialogflow, Used for : 
1. NLP services : intent detection and labelling.
2. UI integration : to display Rich Responses(Accordions and Chips) returned from the server via a Webhook.
- Scrapy : Used to regularly update the NGO database by crawling NGOsIndia website and writing data to mySQL.
