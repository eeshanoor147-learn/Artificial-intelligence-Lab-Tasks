movies = [
 ("Eternal Sunshine of the Spotless Mind", 20000000),
 ("Memento", 9000000),
 ("Requiem for a Dream", 4500000),
 ("Pirates of the Caribbean: On Stranger Tides", 379000000),
 ("Avengers: Age of Ultron", 365000000),
 ("Avengers: Endgame", 356000000),
 ("Incredibles 2", 200000000)
]

total_budget=0
for movie in movies:
    total_budget+=movie[1]
aver_budget=total_budget/len(movies) 
print("Average budget=",aver_budget)

print("Movies which has higher budget then average budget are:")   
for movie in movies:
    if movie[1]>aver_budget:
        print( movie) 
        
print("how much higher the movie's budget then average")        
for movie in movies:
    if movie[1]>aver_budget:
        difference=movie[1]-aver_budget
        print(movie[0],"is greater then average by:",difference)
        
count=0        
for movie in movies:
    if movie[1]>aver_budget:  
        count+=1
print("The number of movies which have higher budget than average budget are:", count )   

# short code
movies = [
 ("Eternal Sunshine of the Spotless Mind", 20000000),
 ("Memento", 9000000),
 ("Requiem for a Dream", 4500000),
 ("Pirates of the Caribbean: On Stranger Tides", 379000000),
 ("Avengers: Age of Ultron", 365000000),
 ("Avengers: Endgame", 356000000),
 ("Incredibles 2", 200000000)
]
print("1.to add more movies")
print("2.simply run no add more movies")
choice=input("Enter the choice:")
if choice =="1":
    add_more_movies=input("Enter more movies")
# method 2
total_budget=0
for movie in movies:
    total_budget+=movie[1]
aver_budget=total_budget/len(movies) 
print("Average budget=",aver_budget) 

count=0
print("Movies which has higher budget then average budget are:") 
for movie in movies:
    if movie[1]>aver_budget:
        differ=movie[1]-aver_budget
        print(movie[0],"is greater then average by:",differ)
        count+=1       
print("The number of movies which have higher budget than average budget are:", count )   
 