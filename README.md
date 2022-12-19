# F22-Cloud-Project_MS1-Students
Microservice 1 - Students

Schema for table Candidates:

<img width="601" alt="Screen Shot 2022-12-18 at 11 18 40 PM" src="https://user-images.githubusercontent.com/19955618/208346775-85b92a08-39d2-4eb6-9b65-85538c2b70e6.png">


## Endpoints: 
`/api/candidates/<id>`

Response:  
```javascript
{  
  "id": "randomstring",
  "first_name": "John",      
  "last_name": "Doe",    
  "email": "jdoe@columbia.edu",  
  "created_on": "1", 
  "last_login" : ""
}
```

`/api/candidates`

Response: 
```javascript
[{  
  "id": "randomstring",
  "first_name": "John",      
  "last_name": "Doe",    
  "email": "jdoe@columbia.edu",  
  "created_on": "1", 
  "last_login" : ""
}, {...}, {...}] 
```

`/api/health` - to check for the status of the microservice.  
Expected respone: 
```javascript
{
  "name": "Candidate-Microservice",
  "health": "Good",
  "at time": <current_time>
}
```


