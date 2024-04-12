Admin Features:
    Manage Project:
        Projects Database:
            localhost:8080/API/v1/project/id/1
            [Post, Put, Get, Delete]
        Create Project:
            POST localhost:8080/API/v1/projects
	    Request:
     		POST /API/v1/projects HTTP/1.1
                Host: localhost:8080
                Content-Type: application/json
                {
		  "id": ObjectId,
		  "name": "Project Name",
		   "key": "Project Initials",
		   "type": "Team-managed business",
		  “lead”: ObjectId("UserID")
                }
	     Response:
                {
                    "success": true,
                    "msg": "Project created successfully.",
                    "project": {
	      		  "id": ObjectId,
			  "name": "Project Name",
			   "key": "Project Initials",
			   "type": "Team-managed business",
			  “lead”: ObjectId("UserID")
                    }
                }
	Project setting:
 	    PUT loclalhost:8080/API/v1/projects?id=x&name=y&key=a&type=b&lead=c
      	Last Issue Update:
       	    PATCH loclalhost:8080/API/v1/projects/id/lastIssueUpdates
        Search Project:
            GET localhost:8080/API/v1/projects?id
	    response:
     		{
                    "success": true,
                    "projects": {
	      		  "id": ObjectId,
			  "name": "Project Name",
			  "key": "Project Initials",
			  "type": "Team-managed business",
			  "lead": ObjectId("UserID")
        	}
        Delete Project:
            Delete localhost:8080/API/v1/projects?id
	    Request:
		DELETE /API/v1/projects?id=项目ID HTTP/1.1
		Host: localhost:8080
		Content-Type: application/json
		Authorization: Bearer your_access_token
  	    Response:
       		{
		    "status": "success",
		    "msg": "Project deleted successfully"
		}
        List Project Table:
            GET localhost:8080/API/v1/projects
	    Response:
     		              {
                    "success": true,
                    "projects": [
                        {
                            "id": "101",
                            "name": "exampleProject1",
			    "key": "Project Initials",
			    "type": "Team-managed business",
			    "lead": ObjectId("UserID")
                        },
                        {
                            "id": "102",
                            "name": "AI for Healthcare",
		  	    "key": "Project Initials",
			    "type": "Team-managed business",
			    "lead": ObjectId("UserID")
                        }
                    ]
                }
    Product Access:
    	Product Database:
     	    localhost:8080/API/v1/access
            [Post, Put, Get, Delete]
 	PUT localhost:8080/API/v1/accesses?User_id=1&useradmin=2&productadmin=3
    User Management:
        Users Database:
            localhost:8080/API/v1/User/id/1
            [Post, Put, Get, Delete]
            localhost:8080/API/v1/Users
        Invite User: (send user invitation by email)
            POST localhost:8080/API/v1/boards/id/members
	    Request:
     		{
		  "email": "example@ex.com"
		}
     	    Response:
	  	{
		  "status": "success",
		  "message": "User invited successfully to the board."
		}
  		or
    		{
		  "status": "error",
		  "message": "User with the provided email not found."
		}
        List User Table:
            GET localhost:8080/API/v1/boards/board_Id/memebers
     	    Response:
		{
		    "status": "success",
		    "data": [
		        {
		            "_id": "userId1",
		            "name": "User Name 1",
		            "email": "user1@example.com"
		        },
		        {
		            "_id": "userId2",
		            "name": "User Name 2",
		            "email": "user2@example.com"
		        }
		    ]
		}
        User status:
            GET localhost:8080/API/v1/Users/Userid?status
     	    Response:
		{
	    		"status": "online"
		}
        Update User Last active:
            GET localhost:8080/API/v1/Users/UserId?lastActive=datetime
     	    Response:
		{
	    		"last_active": "datetime"
		}

            PATCH localhost:8080/API/v1/Users/UserId?LastActive=datetime
	    Request:
     		PATCH /API/v1/Users/{UserId} HTTP/1.1
		Host: localhost:8080
		Content-Type: application/json
		Authorization: Bearer your_access_token
		
		{
		    "last_active": "2024-04-12T15:00:00Z"
		}
     	    Response:
	  	{
		    "status": "success",
		    "msg": "Last active time updated successfully."
		}
        User Detailed Name Card:
            GET localhost:8080/API/v1/Users?UserId=1&fullname=zhiyuanguo&emailaddress=example@exm.com&publicname=Lambton42&initials=zy&status=online&lastactive=datetime
	    Response:
		{
		    "_id": "1",
		    "full_name": "Zhiyuan Guo",
		    "public_name": "Lambton42",
		    "initials": "zy",
		    "email": "example@exm.com",
		    "status": "online",
		    "last_active": "2024-04-12T15:00:00Z"
		}
    Task Board Management:
        Tasks Database:
            localhost:8080/API/v1/task/task_id/1
            [Post, Put, Get, Delete]
            localhost:8080/API/v1/tasks
        Task Search:
	    GET localhost:8080/API/v1/tasks?task_id=1
     	    Response:
		{
		  "_id": "uniqueIdHere",
		  "name": "Task Title",
		  "description": "Task Description",
		  "total_order_id": "projectIdHere",
		  "assignee": "userIdHere",
		  "reporter": "userIdHere",
		  "priority": "high",
		  "start_date": "2024-04-05T09:00:00",
		  "due_date": "2024-04-10T09:00:00",
		  "status_id": "status_id",
		  "activity": {
		    "comments": [
		      {
		        "_id": "uniqueIdHere",
		        "timestamp": "2024-04-05T09:15:00",
		        "user_id": "userId",
		        "Initials": "JD",
		        "comment": "This is a sample comment."
		      }
		    ],
		    "history": [
		      {
		        "_id": "uniqueIdHere",
		        "timestamp": "2024-04-05T09:30:00",
		        "user": "userIdHere",
		        "Initials": "JD",
		        "event": "Task created"
		      }
		    ],
		    "actions": [
		      {
		        "link issue": [
		          {
		            "_id": "uniqueIdHere",
		            "timestamp": "2024-04-07T11:30:00Z",
		            "link_id": "projectIdHere"
		          }
		        ],
		        "attached file": [
		          {
		            "_id": "uniqueIdHere",
		            "timestamp": "2024-04-08T14:00:00",
		            "file_name": "example.txt"
		          }
		        ]
		      }
		    ]
		  }
		}
        Task Filter:
            GET localhost:8080/API/v1/tasks?assignee=userId
	    Response:
     		[
		  {
		    "_id": "taskId1",
		    "name": "Task Title 1",
		    "description": "Task Description 1",
		    "total_order_id": "projectIdHere",
		    "assignee": "userIdHere",
		    "reporter": "anotherUserId",
		    "priority": "high",
		    "start_date": "2024-04-05T09:00:00",
		    "due_date": "2024-04-10T09:00:00",
		    "status_id": "active",
		    "activity": {
		      "comments": [
		        {
		          "_id": "commentId1",
		          "timestamp": "2024-04-05T09:15:00",
		          "user_id": "userId",
		          "Initials": "JD",
		          "comment": "Initial task setup."
		        }
		      ],
		      "history": [
		        {
		          "_id": "historyId1",
		          "timestamp": "2024-04-05T09:30:00",
		          "user": "userIdHere",
		          "Initials": "JD",
		          "event": "Task created"
		        }
		      ]
		    }
		  },
		  {
		    "_id": "taskId2",
		    "name": "Task Title 2",
		    "description": "Task Description 2",
		    "total_order_id": "anotherProjectId",
		    "assignee": "userIdHere",
		    "reporter": "userIdHere",
		    "priority": "low",
		    "start_date": "2024-04-06T10:00:00",
		    "due_date": "2024-04-12T17:00:00",
		    "status_id": "planning",
		    "activity": {}
		  }
		]
        assignee:
            GET localhost:8080/API/v1/tasks/task_id/assigneeuserId
	    Response:
     		{
       			"assignee": "userIdHere"
		}
        Status Column Data:
            GET localhost:8080/API/v1/boards/board_id/tasks/key
	    Response:
     		{
       			"key": "KEY-11"
		}
        Status Rename:
            PATCH localhost:8080/API/v1/tasks?name=name
	    Request:
     		PATCH /API/v1/tasks/taskId HTTP/1.1
		Host: localhost:8080
		Content-Type: application/json
		Authorization: Bearer your_access_token
		
		{
		    "name": "New Task Name"
		}
     	    Response:
		  {
		    "status": "success",
		    "msg": "Task renamed successfully."
		  }
        Status delete:
            DELETE localhost:8080/API/v1/tasks?id=1
	    Request:
     		DELETE /API/v1/tasks?id=1 HTTP/1.1
		Host: localhost:8080
		Authorization: Bearer your_access_token
     	    Response:
		  {
		    "status": "success",
		    "msg": "Task deleted successfully."
		  }
        Copy link:
            GET localhost:8080/API/v1/tasks/task_id?link
	    Response:
		{
		    "status": "success",
		    "link": "https://localhost:8080/tasks/view/task_id"
		}

        Task card actions delete:
            DELETE localhost:8080/API/v1/tasks?id=1
	    Request:
	     	DELETE /API/v1/tasks?id=1 HTTP/1.1
		Host: localhost:8080
		Authorization: Bearer your_access_token
     	    Response:
		{
		    "status": "success",
		    "msg": "Task deleted successfully."
		}
	Task details:
 	    Get localhost:8080/API/v1/tasks/Title/Assignee/DueDate/TaskNumber?priority=high/medium/low
      	    Response:
		    {
		        "_id": "taskId1",
		        "title": "Project Launch",
		        "assignee": "LeonQC",
		        "dueDate": "2024-04-10",
		        "taskNumber": "123",
		        "priority": "high",
		        "description": "Details about the task..."
		    }
      	    PATCH localhost:8080/API/v1/tasks/task_id/Assignee/assignee_id?DueDate=datetime&TaskNumber=18&priority=high/medium/low
	    Request:
		PATCH /API/v1/tasks/task_id HTTP/1.1
		Host: localhost:8080
		Content-Type: application/json
		Authorization: Bearer your_access_token
		
		{
		    "assignee_id": "assignee_id",
		    "dueDate": "2024-04-10T00:00:00Z",
		    "taskNumber": 18,
		    "priority": "high"
		}
     	    Response:
	  	{
		    "status": "success",
		    "msg": "Task updated successfully.",
		    "task": {
		        "id": "task_id",
		        "assignee_id": "assignee_id",
		        "dueDate": "2024-04-10T00:00:00Z",
		        "taskNumber": 18,
		        "priority": "high"
		    }
		}
	Total number of tasks in this column:
 	    GET localhost:8080/API/v1/boards/board_Id/columns/name?count
      	    Response:
		{
		    "status": "success",
		    "column_name": "column_name",
		    "task_count": 10
		}
    Task Content:
        Create new task:
            POST localhost:8080/API/v1/tasks
	    Request:
		POST /API/v1/tasks HTTP/1.1
		Host: localhost:8080
		Content-Type: application/json
		Authorization: Bearer your_access_token
		  {
		  "name": "Task Title",
		  "description": "Task Description",
		  "total_order_id": "projectIdHere",  // This should be the actual project ID
		  "assignee": "userIdHere",           // This should be the actual user ID of the assignee
		  "reporter": "userIdHere",           // This should be the actual user ID of the reporter
		  "priority": "high",
		  "start_date": "2024-04-05T09:00:00Z",
		  "due_date": "2024-04-10T09:00:00Z",
		  "status_id": "status_id",           // Status of the task (e.g., open, in progress, completed)
		  "activity": {
		    "comments": [
		      {
		        "timestamp": "2024-04-05T09:15:00Z",
		        "user_id": "userId",
		        "Initials": "JD",
		        "comment": "Initial setup of task."
		      }
		    ],
		    "history": [
		      {
		        "timestamp": "2024-04-05T09:30:00Z",
		        "user": "userIdHere",
		        "Initials": "JD",
		        "event": "Task created"
		      }
		    ],
		    "actions": [
		      {
		        "link issue": [
		          {
		            "timestamp": "2024-04-07T11:30:00Z",
		            "link_id": "projectIdHere"
		          }
		        ],
		        "attached file": [
		          {
		            "timestamp": "2024-04-08T14:00:00Z",
		            "file_name": "example.txt"
		          }
		        ]
		      }
		    ]
		  }
		}

     	    Response:
	  	HTTP/1.1 201 Created
		Content-Type: application/json
		
		{
		  "status": "success",
		  "msg": "Task created successfully.",
		  "task_id": "uniqueIdGeneratedByDatabase"
		}
        Task Title: 
	    GET localhost:8080/API/v1/tasks/title
     	    Response:
		  {
		    "title": "The specific task title"
		  }
        Description:
	    GET localhost:8080/API/v1/tasks/description
     	    Response:
	   	{
		    "description": "Task Description"
		}
     	    PATCH localhost:8080/API/v1/tasks?description=des
	    Request:
     		PATCH /API/v1/tasks/task_id HTTP/1.1
		Host: localhost:8080
		Content-Type: application/json
		Authorization: Bearer your_access_token
		
		{
		    "description": "New description here"
		}
     	    Response:
	  	HTTP/1.1 200 OK
		Content-Type: application/json
		
		{
		    "status": "success",
		    "msg": "Task description updated successfully."
		}
        Activity:
            Comments: 
                GET localhost:8080/API/v1/tasks/task_id/comments/commentId
		Response:
		  {
		    "_id": "commentId",
		    "timestamp": "2024-04-05T09:15:00",
		    "user_id": "userId",
		    "Initials": "JD",
		    "comment": "This is the text of the comment."
		}
                POST localhost:8080/API/v1/tasks/task_id/comments
		Request:
  			POST /API/v1/tasks/task_id/comments HTTP/1.1
			Host: localhost:8080
			Content-Type: application/json
			Authorization: Bearer your_access_token
			
			{
			    "user_id": "userIdHere",
			    "Initials": "InitialsHere",
			    "comment": "Your comment text here"
			}
     	    	Response:
	   		{
			    "status": "success",
			    "msg": "Comment added successfully.",
			    "comment": {
			        "_id": "newCommentId",
			        "user_id": "userIdHere",
			        "Initials": "InitialsHere",
			        "timestamp": "2024-04-12T12:00:00Z",
			        "comment": "Your comment text here"
			    }
			}

                DELETE localhost:8080/API/v1/tasks/task_id/comments?commentId=1	
		Request:
  			DELETE /API/v1/tasks/task_id/comments/commentId HTTP/1.1
			Host: localhost:8080
			Authorization: Bearer your_access_token
     	    	Response:
	   		HTTP/1.1 204 No Content for successfully deleting
            History: 
                GET localhost:8080/API/v1/tasks/task_id/history 
		Response:
  			{
			    "task_id": "task_id",
			    "history": [
			        {
			            "_id": "historyId1",
			            "timestamp": "2024-04-05T09:30:00Z",
			            "user": "userIdHere",
			            "Initials": "JD",
			            "event": "Task created"
			        },
			        {
			            "_id": "historyId2",
			            "timestamp": "2024-04-06T10:15:00Z",
			            "user": "userIdHere",
			            "Initials": "JD",
			            "event": "Task updated",
			            "details": "Priority changed from Medium to High"
			        },
			        // More history entries can be listed here
			    ]
			}
        Action:
            Attachment:
                POST localhost:8080/API/v1/tasks/task_id/attached files/attached file_id
		Request:POST /API/v1/tasks/task_id/attached_files HTTP/1.1
			Host: localhost:8080
			Authorization: Bearer your_access_token
			Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
			
			------WebKitFormBoundary7MA4YWxkTrZu0gW
			Content-Disposition: form-data; name="file"; filename="example.txt"
			Content-Type: text/plain
			
			(data of the file)
			------WebKitFormBoundary7MA4YWxkTrZu0gW--
      		Response:
			{
			    "status": "success",
			    "msg": "File attached successfully.",
			    "attached_file": {
			        "task_id": "task_id",
			        "file_id": "newlyGeneratedFileId",
			        "filename": "example.txt",
			        "url": "https://localhost:8080/path/to/file/example.txt"
			    }
			}
                DELETE localhost:8080/API/v1/tasks/task_id/attached files?attached file_id
		Request:
  			DELETE /API/v1/tasks/task_id/attached_files/file_id HTTP/1.1
			Host: localhost:8080
			Authorization: Bearer your_access_token
      		Response:
			HTTP/1.1 204 No Content
        



