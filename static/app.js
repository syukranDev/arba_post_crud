$(document).ready(function() {

    const $loginForm = $("#loginForm");
    const $registerButton = $("#registerButton");
    const $createPostButton = $("#createPostButton");
    const $createCommentButton = $("#createCommentButton");
    const $postList = $("#postList");
    const $commentList = $("#commentList");

    if ($loginForm.length) {
        //======================================
        // =========== Login API
        //======================================
        $loginForm.on("submit", function(event) {
            event.preventDefault();
            const username = $("#username").val();
            const password = $("#password").val();

            $.ajax({
                url: '/api/login',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ username, password }),
                success: function(result) {
                    console.log('===================')
                    console.log(result)
                    sessionStorage.setItem('token', result.token);
                    sessionStorage.setItem('user_id', result.user_id);
                    // Redirect to posts page
                    window.location.href = '/posts';
                },
                error: function(jqXHR) {
                    $("#errorMessage").text(jqXHR.responseJSON.message);
                }
            });
        });

        //======================================
        //=========== Register API
        //======================================
        $registerButton.on("click", function() {
            const username = $("#username").val();
            const password = $("#password").val();

            $.ajax({
                url: '/api/register',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ username, password }),
                success: function(result) {
                    alert("Registration successful! You can now log in.");
                },
                error: function(jqXHR) {
                    $("#errorMessage").text(jqXHR.responseJSON.message);
                }
            });
        });


    }

    // ==========================================================================================
    // Post related logic
    // ==========================================================================================
    if ($postList.length) {
        loadPosts();
    }

    function loadPosts() {
        const token = sessionStorage.getItem('token'); 
        const user_id = sessionStorage.getItem('user_id'); 

        $.ajax({
            url: '/api/posts/list',
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` 
            },
            success: function(posts) {
                $postList.empty(); 
                posts.forEach(post => {
                    const $li = $(`<li style="margin-top:10px">ID: ${post.id} <br>Title: ${post.title} <br> Content: ${post.content} <br> Posted By: ${post.user_id}</li>`);
                    const $showCommentsButton = $('<button style="margin-left:10px">Show Comments</button>');
                    $showCommentsButton.on('click', () => {
                        window.location.href = `/posts/${post.id}/comments`;
                    });

                    if (user_id == post.user_id)
                    {
                        const $editButton = $('<button style="margin-left:10px">Edit</button>');
                        $editButton.on('click', () => editPost(post.id));
                        const $deleteButton = $('<button style="margin-left:5px">Delete</button>');
                        $deleteButton.on('click', () => deletePost(post.id));
                        $li.append($editButton).append($deleteButton);
                    }
                    $li.append($showCommentsButton)
                    $postList.append($li);
                });
            },
            error: function(err) {
                console.log(err)
                alert(err.responseJSON.message);
            }
        });
    }
    
    $createPostButton.on("click", function() {
        const title = prompt("Enter post title:");
        const content = prompt("Enter post content:");
        const token = sessionStorage.getItem('token'); 

        $.ajax({
            url: '/api/posts/create',
            method: 'POST',
            contentType: 'application/json',
            headers: {
                'Authorization': `Bearer ${token}` 
            },
            data: JSON.stringify({ title, content }),
            success: function() {
                loadPosts();
            },
            error: function(err) {
                alert(err.responseJSON.errMsg);
            }
        });
    });

    function editPost(postId) {
        const newTitle = prompt("Enter new title:");
        const newContent = prompt("Enter new content:");
        const token = sessionStorage.getItem('token'); 
        $.ajax({
            url: `/api/posts/update/${postId}`,
            method: 'POST',
            contentType: 'application/json',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            data: JSON.stringify({ title: newTitle, content: newContent }),
            success: function() {
                loadPosts();
            },
            error: function(err) {
                console.log(JSON.stringify(err.responseJSON))
                alert(err.responseJSON);
            }
        });
    }

    function deletePost(postId) {
        const token = sessionStorage.getItem('token'); 
        $.ajax({
            url: `/api/posts/delete/${postId}`,
            method: 'GET', 
            headers: {
                'Authorization': `Bearer ${token}` 
            },
            success: function(d) {
                console.log(d)
                console.log(JSON.stringify(d))
                alert(d.message)
                loadPosts(); 
            },
            error: function(err) {
                console.log(JSON.stringify(err.responseJSON))
                alert(err.responseJSON);
            }
        });
    }

     // ==========================================================================================
    // Comment related logic
    // ==========================================================================================
    if ($commentList.length) {
        const postId = $("#postId").val();
        loadComments(postId);
    }

    function loadComments(postId) {
        const token = sessionStorage.getItem('token'); 
        const user_id = sessionStorage.getItem('user_id'); 

        $.ajax({
            url: `/api/posts/${postId}/comments/list`,
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` 
            },
            success: function(comments) {
                $commentList.empty(); 
                console.log(comments)
                if (comments.length > 0) {
                    comments.forEach(comment => {
                        const $li = $(`<li style="margin-top:5px">${comment.content} - (by: ${comment.user_id})</li>`); // Adjust based on your comment object
                        if (user_id == comment.user_id) {
                            const $editButton = $('<button style="margin-left:10px">Edit</button>');
                            $editButton.on('click', () => editComment(comment.id));
                            const $deleteButton = $('<button style="margin-left:10px">Delete</button>');
                            $deleteButton.on('click', () => deleteComment(comment.id));
                            $li.append($editButton).append($deleteButton);
                        }
                        $commentList.append($li);
                    });
                }
            }
        });
    }

    $createCommentButton.on("click", function() {
        const postId = $("#postId").val();
        console.log(postId)

        const content = prompt("Enter comment for this post:");
        const token = sessionStorage.getItem('token'); 

        $.ajax({
            url: `/api/posts/${postId}/comments/create`,
            method: 'POST',
            contentType: 'application/json',
            headers: {
                'Authorization': `Bearer ${token}` 
            },
            data: JSON.stringify({ content }),
            success: function() {
                loadComments(postId);
                alert('Successfully added')
            },
            error: function(err) {
                alert(err.responseJSON.errMsg);
            }
        });
    });

    function editComment(commentId) {
        const postId = $("#postId").val();
        const newContent = prompt("Enter new comment:");
        const token = sessionStorage.getItem('token'); 
        $.ajax({
            url: `/api/comments/${commentId}/update`,
            method: 'POST',
            contentType: 'application/json',
            headers: {
                'Authorization': `Bearer ${token}` 
            },
            data: JSON.stringify({ content: newContent }),
            success: function() {
                loadComments(postId); 
            }
        });
    }

    function deleteComment(commentId) {
        const postId = $("#postId").val();
        const token = sessionStorage.getItem('token'); 
        $.ajax({
            url: `/api/comments/${commentId}/delete`,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}` 
            },
            success: function() {
                loadComments(postId); 
            }
        });
    }
});
