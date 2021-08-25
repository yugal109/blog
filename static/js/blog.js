

  axios.defaults.xsrfCookieName = "csrftoken";
  axios.defaults.xsrfHeaderName = "X-CSRFToken";


    const postLike = (id) => {
    // axios.defaults.xsrfCookieName = "csrftoken";
    // axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios
      .post(`http://localhost:8000/blog/like/${id}`, {
        csrfmiddlewaretoken: "{{ csrf_token }}",
      })
      .then((response) => {
        if (response.data.liked) {
          document.getElementById(`likesof${id}`).innerHTML = `
              <button onClick="postUnlike('${id}')"  style="background-color: white">
                <img
                  style="width:50px;height:50px"
                  src="/media/icons/redheart.png"
                />
              </button>
      `;
          document.getElementById(`likeslength`).innerHTML++;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const postUnlike = (id) => {
    // axios.defaults.xsrfCookieName = "csrftoken";
    // axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios
      .post(`http://localhost:8000/blog/unlike/${id}`)
      .then((response) => {
        if (response.data.liked == false) {
          document.getElementById(`likesof${id}`).innerHTML = `
              <button onClick="postLike('${id}')"  style="background-color: white">
                <img
                  style="width:50px;height:50px"
                  src="/media/icons/heart.png"
                />
              </button>
      `;
          document.getElementById(`likeslength`).innerHTML--;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };






  // UPDATE COMMETN 
    const updateComment = (id) => {
      console.log(id)

    axios.post(`http://localhost:8000/blog/updatecomment/${id}`,{
      'comment':document.getElementById(`updateCommentField${id}`).value
    })
    .then((response)=>{
      document.getElementById(`actualComment${id}`).innerHTML=response.data.comment
      document.getElementById(`exampleModalCenter${id}`).className="modal fade"
      document.querySelector(".modal-backdrop").className="modal-backdrop fade"
    
    })
    .catch((error)=>{
      console.log(error)
    })
  
  };



  // DELET REPLY
  const deleteReply = (id) => {
    axios
      .post(`http://localhost:8000/blog/deletereply/${id}`)
      .then((response) => {
        console.log(response.data);
        if (response.data.deletion) {
          document.getElementById(`replyid${id}`).innerHTML = ``;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };


  //COMMENT
  const comment = () => {
    const id = document.getElementById("postId").value;
  
    console.log(document.getElementById("comment_field").value);
    const comments_list = document.getElementById("commets_list");

    axios
      .post(`http://localhost:8000/blog/com/${id}`, {
        comment: document.getElementById("comment_field").value,
      })
      .then((response) => {
        console.log(response.data);
        const comment_id = response.data.comment_id;
        const comment = JSON.parse(response.data.comment)[0].fields;
        const user = JSON.parse(response.data.user)[0].fields;
        const profile = JSON.parse(response.data.profile)[0].fields;

        comments_list.innerHTML += `

  <div id="commentid${comment_id}" class="full comment_blog_line">
          <div class="row">
            <div class="col-md-1">
              

              <img style="  vertical-align: middle;
              width: 80px;
              height: 70px;
              border-radius: 50%;" src=${profile.image} alt="Avatar" class="avatar">
            </div>
            <div  class="col-md-9">
              <div class="full contact_text">
                <div style="display: flex;align-items: center;margin-bottom:10px">
                <h3>${user.username}</h3>
                <div style="margin-left: 5px;">
                  <button
                      style="
                        padding: 2px;
                        color: white;
                        font-weight: 600;
                        background-color: rgb(54, 190, 190);
                      "
                      data-toggle="modal" data-target="#exampleModalCenter${comment_id}">
                      Update
                    </button>
                  <button onclick="deleteComment('${comment_id}')" style="padding:2px;color:white;font-weight: 600;background-color: red;">Delete</button>
                  </div>

                     <div class="modal fade" id="exampleModalCenter${comment_id}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="exampleModalLongTitle">Modal title</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                      </button>
                    </div>
                    <div class="modal-body">
                      <div>
                        <input id="updateCommentField${comment_id}" type="text" value="${comment.comment}" >
                      </div>
                    </div>
                    <div style="padding:10px">
                     <button onclick="updateComment('${comment_id}')" id="updateButton">Update</button>
                    </div>
                  </div>
                </div>
              </div>

              </div>
                <h4>Posted on Jan 10 / 2017 at 06:53 am</h4>
                <p>
                  <div id="actualComment${comment_id}">
                ${comment.comment}
                </div>
                  <div id="likescommentid${comment_id}">
                    <button name="likecomment" 
                              onClick="commentLike('${comment_id}')" 
                              style="background-color: white">
                                <img
                                  style="width: 18px; height: 18px"
                                  src="/media/icons/heart.png"
                                />
                              </button>
                              <input hidden name="comid" type="text" value=${comment_id} />
    
                  </div>
                
                 0 replies in this comment.
                </p>
              </div>
            </div>
        
            <button type="button"  onClick="showReply('${comment_id}')" class="reply_bt">Show Replies</button>
  
            <div id="repliesof${comment_id}" style="display:none;">
              <h3>Replies</h3>
              <hr/>
                   
                <div id="replies_list${comment_id}" >

                </div>
            
            <div id="idof${comment_id}"  style="display: flex;flex-direction: column;justify-content: flex-start;">
             
              </div>
            </div>
          </div>
        </div>
<hr/>
  
  `;
        document.getElementById("comment_field").value = "";

        document.getElementById("comment_length").innerHTML++;
      })
      .catch((error) => {
        console.log(error);
      });
  };


//REPLYYYYYYYYY
  const reply = (id) => {
    const reply_list = document.getElementById(`replies_list${id}`);

    axios
      .post(`http://localhost:8000/blog/reply/${id}`, {
        reply: document.getElementById(`reply${id}`).value,
      })
      .then((response) => {
        const reply_id = response.data.reply_id;

        const reply = JSON.parse(response.data.reply)[0].fields;
        const user = JSON.parse(response.data.user)[0].fields;
        const profile = JSON.parse(response.data.profile)[0].fields;

        reply_list.innerHTML += `

                <div id="replyid${reply_id}" style="display: flex;">
                    <div  class="col-md-1">
                      <img src="${profile.image}" alt="#" />

                    </div>
                    <div  class="col-md-9">
                    <div>
                      <div style="display: flex;align-items: center;margin-bottom:10px">
                        <h3>${user.username}</h3>
                        <div style="margin-left: 5px;">

                    <button
                    data-toggle="modal" data-target="#exampleModalCenter${reply_id}" 
                      style="
                        padding: 2px;
                        color: white;
                        font-weight: 600;
                        background-color: rgb(54, 190, 190);
                      "
                      >
                      Update
                    </button>
                    <button onclick="deleteReply('${reply_id}')" style="padding:2px;color:white;font-weight: 600;background-color: red;">Delete</button>
                    </div>


                <div class="modal fade" id="exampleModalCenter${reply_id}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="exampleModalLongTitle">Modal title</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                      </button>
                    </div>
                    <div class="modal-body">
                      <div>
                        <input id="updateReplyField${reply_id}" type="text" value="${reply.reply}" >
                      </div>
                    </div>
                    <div style="padding:10px">
                     <button onclick="updateReply('${reply_id}')" id="updateButton">Update</button>
                    </div>
                  </div>
                </div>
              </div>
                        
                      </div>
                      <h6>Posted on Jan 10 / 2017 at 06:53 am</h6>
                      <!-- < style="font-size: 14px;"> -->
                      <div id="likerepliesid${reply_id}">
                      
                        <button
                          name="likereply"
                          type="submit"
                          style="background-color: white"
                          onClick="replyLike('${reply_id}')"

                        >
                          <img
                            style="width: 18px; height: 18px"
                            src="/media/icons/heart.png"
                          />
                        </button>
                        <input
                          hidden
                          name="repid"
                          type="text"
                          value="${reply_id}"
                        />
                       
                      </div>
                      <div id="actualReply${reply_id}">
                      ${reply.reply}
                     </div>
                     </div>
                  </div>
                  <hr/>
</div>
        `;
        document.getElementById(`reply${id}`).value = "";
      })
      .catch((error) => {
        console.log(error);
      });
  };

  let show = true;
  function showReply(name) {

    console.log("the show is ",show)

    if (show == true) {
      document.getElementById(`repliesof${name}`).style.display = "block";

      document.getElementById(`idof${name}`).innerHTML = `
          <input id="reply${name}" name="reply" type="text" placeholder="Reply" />
          <button onClick="reply('${name}')"  name="reply_button"  class="reply_bt">Reply</button>
          <input name="comment_id" value=${name} type="text" hidden /> 
          <input name="reactor_id" value=${name} type="text" hidden /> 
          `  
      show =false
    } else {
      document.getElementById(`repliesof${name}`).style.display = "none";
      // $(".modal").modal("hide")
      show = true;
    }
  }



  const deleteComment = (id) => {
    axios
      .post(`http://localhost:8000/blog/deletecomment/${id}`)
      .then((response) => {
        console.log(response.data);
        if (response.data.deletion) {
          document.getElementById(`commentid${id}`).innerHTML = ``;
          document.getElementById("comment_length").innerHTML--;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };


  const replyLike = (id) => {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    console.log(id);
    axios
      .post(`http://localhost:8000/blog/reply/like/${id}`)
      .then((response) => {
        if (response.data.liked) {
          document.getElementById(`likerepliesid${id}`).innerHTML = `
              <button onClick="replyUnlike('${id}')"  style="background-color: white">
                <img
                  style="width: 18px; height: 18px"
                  src="/media/icons/redheart.png"
                />
              </button>
      `;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const replyUnlike = (id) => {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";

    console.log(id);
    axios
      .post(`http://localhost:8000/blog/reply/unlike/${id}`)
      .then((response) => {
        if (response.data.liked == false) {
          document.getElementById(`likerepliesid${id}`).innerHTML = `
              <button onClick="replyLike('${id}')"  style="background-color: white">
                <img
                  style="width: 18px; height: 18px"
                  src="/media/icons/heart.png"
                />
              </button>
      `;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };



  const commentLike = (id) => {
    document.getElementById(`likescommentid${id}`).innerHTML = `
    <button onClick="commentUnlike('${id}')"  style="background-color: white">
      <img
        style="width: 18px; height: 18px"
        src="/media/icons/redheart.png"
      />
    </button>
`;
document.getElementById(`commentlikeslength${id}`).innerHTML++;
    axios
      .post(`http://localhost:8000/blog/comment/like/${id}`)
      .then((response) => {
        if (response.data.liked) {
      //     document.getElementById(`likescommentid${id}`).innerHTML = `
      //         <button onClick="commentUnlike('${id}')"  style="background-color: white">
      //           <img
      //             style="width: 18px; height: 18px"
      //             src="/media/icons/redheart.png"
      //           />
      //         </button>
      // `;
      //     document.getElementById(`commentlikeslength${id}`).innerHTML++;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const commentUnlike = (id) => {

    document.getElementById(`likescommentid${id}`).innerHTML = `
    <button onClick="commentLike('${id}')"  style="background-color: white">
      <img
        style="width: 18px; height: 18px"
        src="/media/icons/heart.png"
      />
    </button>
`;
document.getElementById(`commentlikeslength${id}`).innerHTML--;
    
    axios
      .post(`http://localhost:8000/blog/comment/unlike/${id}`)
      .then((response) => {
        if (response.data.liked == false) {
      //     document.getElementById(`likescommentid${id}`).innerHTML = `
      //         <button onClick="commentLike('${id}')"  style="background-color: white">
      //           <img
      //             style="width: 18px; height: 18px"
      //             src="/media/icons/heart.png"
      //           />
      //         </button>
      // `;
      // document.getElementById(`commentlikeslength${id}`).innerHTML--;

        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  //all comment likes 
  const showCommentLikes=(id)=>{
  likes_list=document.getElementById("comment_likes_list")
   axios
    .post(`http://localhost:8000/blog/all_likes_comment/${id}`)
    .then((response) => {
      all_likes=JSON.parse(JSON.parse(response.data.likes))
      likes_list.innerHTML=''
      comment_list_of_likes=JSON.parse(JSON.parse(response.data.likes))
      for(let i=0;i<comment_list_of_likes.length;i++){
        likes_list.innerHTML+=
        
        `
        <li class="list-group-item">${comment_list_of_likes[i].fields.username}</li>
        `
        
      }
    })
    .catch((error) => {
      console.log(error);
    });
  }

