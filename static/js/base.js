
      axios.defaults.xsrfCookieName = "csrftoken";
      axios.defaults.xsrfHeaderName = "X-CSRFToken";




      const chatSocket = new WebSocket(
        "ws://" + window.location.host + "/ws/notifications/"
      );
      console.log(window.location.host);
      console.log(chatSocket);

      chatSocket.onmessage = function (e) {
        if (JSON.parse(e.data).notifications) {
          let length = JSON.parse(JSON.parse(e.data).notifications).length;
          document.getElementById("notifications_length").innerHTML = length;
        } else {
          let length = JSON.parse(JSON.parse(e.data).followrequest).length;
          document.getElementById("followrequest_length").innerHTML = length;
        }
      };

      chatSocket.onclose = function (e) {
        console.error("Chat socket closed unexpectedly");
      };

      chatSocket.onerror = (err) => {
        console.log(err);
      };




      console.log(localStorage.getItem("imageURL"))
      if(localStorage.getItem("imageURL")){
        imageURL=JSON.parse(localStorage.getItem("imageURL"))
        console.log("The image is ",imageURL)
        document.getElementById("imageurl").innerHTML=`
                          <img
                          style="
                            vertical-align: middle;
                            width: 50px;
                            height: 50px;
                            border-radius: 50%;
                          "
                          src=${imageURL}
                          alt="A"
                        />`
      }else{
        axios
        .get("http://localhost:8000/blog/imageurl")
        .then((response) => {
          console.log(JSON.stringify(response.data.image))
          localStorage.setItem("imageURL",JSON.stringify(response.data.image))
         
          document.getElementById("imageURL").innerHTML+=`
                          <img
                          style="
                            vertical-align: middle;
                            width: 30px;
                            height: 30px;
                            border-radius: 50%;
                          "
                          src=${response.data.image}
                          alt="A"
                        />
          
          `
          
        })
        .catch((error) => {
          console.log(error);
        });
      }
      


//NOTIFICATIONS LENGTH
      axios
        .get(`http://localhost:8000/blog/notifications_length`)
        .then((response) => {
          document.getElementById("notifications_length").innerHTML =
            response.data.notifications_length;
        })
        .catch((error) => {
          console.log(error);
        });

//FOLLOW REUQESTS LENGTH
      axios
        .get(`http://localhost:8000/blog/followrequest_length`)
        .then((response) => {
          document.getElementById("followrequest_length").innerHTML =
            response.data.followrequest_length;
        })
        .catch((error) => {
          console.log(error);
        });


//NOTIFICATIONS AJAX
let noti_id=document.getElementById("noti_id")

let element = document.getElementById('dropdown2')

noti_id.addEventListener("click",()=>{

if(document.getElementById("dropdown2").style.display=="none")
{
  document.getElementById("dropdown2").style.display="block"

        axios
        .get(`http://localhost:8000/blog/notifications_ajax`)
        .then((response) => {
          notifications=response.data.name
          length=notifications.length
          console.log(notifications)
          for(let i=0;i<length;i++){

                    document.getElementById("dropdown2")
                    .innerHTML+=

                    `
                     
                     <li id="noti${notifications[i].notificationId}" onmouseleave="lightBackground('${notifications[i].notificationId}')" onmouseenter="dimBackground('${notifications[i].notificationId}')" onclick="goToPost('${notifications[i].postId}')" class="list-group-item" style="margin:0 0 0">
                                  <div style="padding:10px">
                                      <div>
                                      <img
                                    style="
                                      vertical-align: middle;
                                      width: 20px;
                                      height: 20px;
                                      border-radius: 50%;
                                    "
                                    src=${notifications[i].image}
                                    alt="A"
                                  />
                                      ${notifications[i].notifications}

                                      </div>
                     </div>
                     </li>
                    
          `

          }
        })
        .catch((error) => {
          console.log(error);
        });


}
else{
  document.getElementById("dropdown2").innerHTML=""

  document.getElementById("dropdown2").style.display="none"
}

})

const dimBackground=(id)=>{
  document.getElementById(`noti${id}`)
  .style.backgroundColor="#DCDCDC"
}

const lightBackground=(id)=>{
  document.getElementById(`noti${id}`)
  .style.backgroundColor="white"
}

const goToPost=(id)=>{
  window.location.href = `http://localhost:8000/blog/blog/${id}`;
}




