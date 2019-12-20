#!/usr/bin/python3

def main(): 
  europe = "Albania | Andorra | Austria | Belarus | Belgium | Bosnia and Herzegovina | Bulgaria | Croatia | Czech Republic | Denmark | Estonia | Faroe Islands | Finland | France | Germany | Gibraltar | Greece | Guernsey | Hungary | Iceland | Ireland | Isle of Man (British Crown dependency) | Italy | Jersey | Kosovo | Latvia | Liechtenstein | Lithuania | Luxembourg | North Macedonia | Malta | Moldova | Monaco | Montenegro | Netherlands | Norway | Poland | Portugal | Romania | Russia | San Marino | Serbia | Slovakia | Slovenia | Spain | Svalbard | Sweden | Switzerland | Ukraine | United Kingdom | Vatican City | Amsterdam, Noord-Holland | Andorra la Vella | Athens, Attiki | Belgrade, Palilula | Berlin | Bern | Bratislava, Bratislavsky | Brussels | Bucharest | Budapest | Chisinau | Copenhagen | Douglas | Dublin | Gibraltar | Helsinki, Uusimaa | Kyiv, Kiev | Lisbon, Lisboa | Ljubljana, Osrednjeslovenska | London, Greater London | Longyearbyen, Svalbard | Luxemburg, Luxembourg | Madrid | Minsk | Monaco | Nicosia | Oslo | Paris, Ile-de-France | Podgorica | Prague, Hlavní město Praha | Pristina | Reykjavik, Hofudhborgarsvaedhi | Riga | Rome, Lazio | Saint Helier | Saint Peter Port | San Marino | Sarajevo, Federacija Bosna i Hercegovina | Skopje | Sofia, Sofia grad | Stockholm | Tallinn, Harju | Tirana | Torshavn, Strømø | Vaduz | Valletta | Vatican City | Vienna | Vilnius, Vilniaus | Warsaw, Mazowieckie | Zagreb, Grad Zagreb"
  
  US = "Montgomery, Alabama | Juneau, Alaska | Phoenix, Arizona | Little Rock, Arkansas | Sacramento, California | Denver, Colorado | Hartford, Connecticut | Dover, Delaware | Tallahassee, Florida | Atlanta, Georgia | Honolulu, Hawaii | Boise, Idaho | Springfield, Illinois | Indianapolis, Indiana | Des Moines, Iowa | Topeka, Kansas | Frankfort, Kentucky | Baton Rouge, Louisiana | Augusta, Maine | Annapolis, Maryland | Boston, Massachusetts | Lansing, Michigan | Saint Paul, Minnesota | Jackson, Mississippi | Jefferson City, Missouri | Helena, Montana | Lincoln, Nebraska | Carson City, Nevada | Concord, New Hampshire | Trenton, New Jersey | Santa Fe, New Mexico | Albany, New York | Raleigh, North Carolina | Bismarck, North Dakota | Columbus, Ohio | Oklahoma City, Oklahoma | Salem, Oregon | Harrisburg, Pennsylvania | Providence, Rhode Island | Columbia, South Carolina | Pierre, South Dakota | Nashville, Tennessee | Austin, Texas | Salt Lake City, Utah | Montpelier, Vermont | Richmond, Virginia | Olympia, Washington | Charleston, West Virginia | Madison, Wisconsin | Cheyenne, Wyoming | Alabama | Alaska | Arizona | Arkansas | California | Colorado | Connecticut | Delaware | District of Columbia | Florida | Georgia | Hawaii | Idaho | Illinois | Indiana | Iowa | Kansas | Kentucky | Louisiana | Maine | Maryland | Massachusetts | Michigan | Minnesota | Mississippi | Missouri | Montana | Nebraska | Nevada | New Hampshire | New Jersey | New Mexico | New York | North Carolina | North Dakota | Ohio | Oklahoma | Oregon | Pennsylvania | Rhode Island | South Carolina | South Dakota | Tennessee | Texas | Utah | Vermont | Virginia | Washington | West Virginia | Wisconsin | Wyoming"

  europe_keywords  = europe.split(" | ")

  US_keywords = US.split(" | ")
  
  keywords = europe_keywords + US_keywords

  query_body = """
    GET film_db/_search
    {
      "query": {
        "bool": {
          "must": [
            {
              "match": { "keywords": "corrupt politician corruption politics ilegal" }
            }
          ],
          "should": [
            { "match": { "description": "USA" } },
            { "match": { "description": "United States" } },
            { "match": { "description": "EU" } },
            { "match": { "description": "Europe" } }"""
  
  query_ending = """\n          ]}},
      "size" : 10
   }
   """

  for i in keywords:
    query_body += """\n           ,{ "match": { "description": \""""+i+"""\" }} """

  query_body += query_ending

  print (query_body)

main()
