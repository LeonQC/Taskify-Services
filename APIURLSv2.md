Admin Features:
    Manage Project:
        Projects Database:
            localhost:8080/API/v1/project/id/1
            [Post, Put, Get, Delete]

        Create Project:
            POST localhost:8080/API/v1/projects/id
            The Request and Response of this POST URL should be:
                POST /API/v1/projects HTTP/1.1
                Host: localhost:8080
                Content-Type: application/json

                {
                    "name": "examplePorject",
                    "startDate": "2024-01-01",
                    "endDate": "2024-12-31",
                    "Assignee": ["12345"]
                    "Reporter": ["45678", "11245"]
                }
            Response:
                {
                    "success": true,
                    "message": "Project created successfully.",
                    "project": {
                        "id": "54321",
                        "name": "New Innovation Project",
                        "description": "This project aims to innovate in the field of renewable energy.",
                        "startDate": "2024-01-01",
                        "endDate": "2024-12-31",
                        "teamMembers": [
                            {
                                "userId": "12345",
                                "role": "Lead"
                            },
                            {
                                "userId": "67890",
                                "role": "Member"
                            }
                        ]
                    }
                }

        Search Project:
            GET localhost:8080/API/v1/projects?search=id
            The Response of this GET URL should be like this:
                {
                    "success": true,
                    "projects": {
                            "id": "12345",
                            "name": "exampleName",
                            "startDate": "2024-01-01",
                            "endDate": "2024-12-31",
                            "Assignee": {
                                    "userId": "67890",
                            },
                            "Reporter": {
                                    "userId": "54321",
                            }
                    }
                }
        Delete Project:
            Delete localhost:8080/API/v1/projects/id
        List Project Table:
            GET localhost:8080/API/v1/projects
            The Response of this Get URL should be like this:

                {
                    "success": true,
                    "projects": [
                        {
                            "id": "101",
                            "name": "exampleProject1",
                            "startDate": "2024-01-01",
                            "endDate": "2024-12-31",
                            "teamMembers": [
                                Assignee: {
                                    "userId": "001",
                                    "name": "Exampel Person1",
                                },
                                Reporter: {
                                    "userId": "002",
                                    "name": "Example Person2",
                                }
                            ]
                        },
                        {
                            "id": "102",
                            "name": "AI for Healthcare",
                            "startDate": "2024-03-01",
                            "endDate": "2025-03-01",
                            "teamMembers": [
                                Assignee: {
                                    "userId": "003",
                                    "name": "Example Person3",
                                },
                                Reporter: {
                                    "userId": "004",
                                    "name": "Example Person4",
                                }
                            ]
                        }
                    ]
                }


    User Management:
        Users Database:
            localhost:8080/API/v1/User/id/1
            [Post, Put, Get, Delete]
            localhost:8080/API/v1/Users
        Invite Member: (send user invitation by email)
            POST localhost:8080/API/v1/projects/id/Users/id
            The Request of the invite url should be like:
                POST /API/v1/Users/invite HTTP/1.1
                Host: localhost:8080
                Content-Type: application/json

                {
                    "email": "User@example.com",
                    "projectId": "id",
                    "inviterId": "id",
                }

            and the Response of this URL should be:

                {
                    "success": true,
                    "message": "Invitation sent successfully.",
                    "projectDetails": {
                    "projectId": "id",
                    "projectName": "exampleName",
                    },
                    "invitedUser": {
                    "email": "User@example.com",
                    "inviterId": "id",
                    }
                }
        List User Table:
            GET localhost:8080/API/v1/projects/id/Users
            The Response of this GET URL should be
            {
                "success": true,
                "projectId": "101",
                "projectName": "ExampleProject1",
                "users": [
                    {
                        "userId": "001",
                        "name": "exampelMember1",
                        "email": "example1@example.com",
                        "role": "Assignee"
                    },
                    {
                        "userId": "002",
                        "name": "exampleMember2",
                        "email": "example2@example.com",
                        "role": "Reporter"
                    },
                    {
                        "userId": "003",
                        "name": "exampleMember3",
                        "email": "example3@example.com",
                        "role": "Reporter"
                    }
                ]
            }       
        User status:
            GET localhost:8080/API/v1/Users/id/status
            The Response of this GET URL should be:
                {
                    "success": true,
                    "userId": "12345",
                    "status": "Active"
                }

        Update User Last active:
            GET localhost:8080/API/v1/Users/id/lastActive
            PATCH localhost:8080/API/v1/Users/id/lastActive
            The request of this specific PATCH URL should be:
                PATCH /API/v1/Users/id/lastActive HTTP/1.1
                Host: localhost:8080
                Content-Type: application/json

                {
                    "lastActive": "2024-04-04 12:34:56"
                }
        User Detailed Name Card:
            GET localhost:8080/API/v1/Users/id/fullname
            GET localhost:8080/API/v1/Users/id/emailaddress
            GET localhost:8080/API/v1/Users/id/publicname
    Task Board Management:
        Tasks Database:
            localhost:8080/API/v1/task/id/1
            [Post, Put, Get, Delete]
            localhost:8080/API/v1/tasks
        Column Search Box:
	        GET localhost:8080/API/v1/tasks?search={keywords}
        Task Filter:
            GET localhost:8080/API/v1/tasks?User=id
        Assignees:
            GET localhost:8080/API/v1/tasks/id/assignee
        Task number:
            GET localhost:8080/API/v1/columns/id/tasks/count
        Three dot actions rename:
            PUT localhost:8080/API/v1/tasks/id/taskname
        Three dot actions delete:
            DELETE localhost:8080/API/v1/tasks/id
        Task card actions copy link:
            GET localhost:8080/API/v1/tasks/id/link
        Task card move position:
            PUT localhost:8080/API/v1/tasks/id/position
        Task card actions delete:
            DELETE localhost:8080/API/v1/tasks/id
        Task title
            GET localhost:8080/API/v1/tasks/id/title
            PUT localhost:8080/API/v1/tasks/id/title
        Task Assignee:
            GET localhost:8080/API/v1/tasks/id/assignee
            PUT localhost:8080/API/v1/tasks/id/assignee
        Task Project initials:
            GET localhost:8080/API/v1/tasks/id/initial
            PUT localhost:8080/API/v1/tasks/id/initial
        No.task:
            GET localhost:8080/API/v1/tasks/id/tasknumber
        Create new task:
            POST localhost:8080/API/v1/tasks/id
    Task Card Details:
        Task Card Status:
            Assignee: 
                GET localhost:8080/API/v1/tasks/id/assignee
                PUT localhost:8080/API/v1/tasks/id/assignee
            Reporter: 
                GET localhost:8080/API/v1/tasks/id/reporter
                PUT localhost:8080/API/v1/tasks/id/reporter
            Priority: 
                GET localhost:8080/API/v1/tasks/id/priority
                PUT localhost:8080/API/v1/tasks/id/priority
            Status: 
                GET localhost:8080/API/v1/tasks/id/status
                PUT localhost:8080/API/v1/tasks/id/status
            Due Date: 
                GET localhost:8080/API/v1/tasks/id/duedate
                PUT localhost:8080/API/v1/tasks/id/duedate
            Category:
                GET localhost:8080/API/v1/tasks/id/category
                PUT localhost:8080/API/v1/tasks/id/category
            Time Tracking: 
                GET localhost:8080/API/v1/tasks/id/timetracking
                PUT localhost:8080/API/v1/tasks/id/timetracking
    Task Content:
        Title: GET localhost:8080/API/v1/tasks/id/title
        Description:GET/PUT localhost:8080/API/v1/tasks/id/description
        Activity:
            Comments: 
                GET localhost:8080/API/v1/tasks/id/comments
                POST localhost:8080/API/v1/tasks/id/comments
                DELETE localhost:8080/API/v1/tasks/id/comments	
            History: 
                GET localhost:8080/API/v1/tasks/id/history
            Work Log: 
                GET/POST localhost:8080/API/v1/tasks/id/worklog/timespent…
        Action:
            Attachment:
                POST localhost:8080/API/v1/tasks/id/attachments
                DELETE localhost:8080/API/v1/tasks/id/attachments
        



