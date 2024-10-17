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

            $('#loadingModal').modal('show');

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
                },
                complete: function() {
                    $('#loadingModal').modal('hide');
                }
            });
        });

        //======================================
        //=========== Register API
        //======================================
        $registerButton.on("click", function() {
            const username = $("#username").val();
            const password = $("#password").val();

            $('#loadingModal').modal('show');

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
                },
                complete: function() {
                    $('#loadingModal').modal('hide');
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

        $('#loadingModal2').modal('show');

        $.ajax({
            url: '/api/posts/list',
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` 
            },
            success: function(posts) {
                $postList.empty(); 
                posts.forEach(post => {
                    const $li = $(`
                        <li class="list-group-item mt-2">
                            <strong>ID:</strong> ${post.id} <br>
                            <strong>Title:</strong> ${post.title} <br> 
                            <strong>Content:</strong> ${post.content} <br> 
                            <strong>Posted By:</strong> ${post.user_id}
                                <button class="btn btn-info btn-sm" style="margin-left:10px">Show Comments</button>
                        </li>
                    `);
    
                    const $showCommentsButton = $li.find('button.btn-info');
                    $showCommentsButton.on('click', () => {
                        window.location.href = `/posts/${post.id}/comments`;
                    });
    
                    if (user_id == post.user_id) {
                        const $editButton = $('<button class="btn btn-warning btn-sm" style="margin-left:10px">Edit</button>');
                        $editButton.on('click', () => editPost(post.id));
                        const $deleteButton = $('<button class="btn btn-danger btn-sm" style="margin-left:5px">Delete</button>');
                        $deleteButton.on('click', () => deletePost(post.id));
                        $li.append($editButton).append($deleteButton);
                    }
                    $postList.append($li);
                });
            },
            error: function(err) {
                console.log(err)
                alert(err.responseJSON.message);
            },
            complete: function() {
                $('#loadingModal2').modal('hide');
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

        $('#loadingModal3').modal('show');
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
                        const $li = $(`
                            <li class="list-group-item mt-2">
                                ${comment.content} - (by: ${comment.user_id})
                                <div class="mt-2">
                                    <button class="btn btn-warning btn-sm" style="margin-left:10px">Edit</button>
                                    <button class="btn btn-danger btn-sm" style="margin-left:5px">Delete</button>
                                </div>
                            </li>
                        `);
    
                        const $editButton = $li.find('button.btn-warning');
                        $editButton.on('click', () => editComment(comment.id));
    
                        const $deleteButton = $li.find('button.btn-danger');
                        $deleteButton.on('click', () => deleteComment(comment.id));
    
                        if (user_id != comment.user_id) {
                            $editButton.hide();
                            $deleteButton.hide();
                        }
    
                        $commentList.append($li);
                    });
                }
            },
            complete: function() {
                $('#loadingModal3').modal('hide');
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
