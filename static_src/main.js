if (document.getElementById('list-product')!=null){
  buildproduct()
}
if ((document.URL.match('basket'))!=null){
  buildbasket()
}
if ((document.URL.match('orders'))!=null){
  buildorders()
}

function countitemsbasket(status) {
  // var wrapper = document.getElementById('count_order')
  // var url = '/api/v1/basket/'
  // fetch(url)
  // .then((resp)=>resp.json())
  // .then(function(data){     
  //   var count = 0
  //   var list = data[0]
  //   for(var i in list){
  //       if (list[i].user_id==data[1] && list[i].status in status) {
  //         count+=1
  // }}
  // wrapper.textContent=count
  // })
}
function updatebasket(list,id){
  var data=list[0]
  console.log(data)
  for(var i in data){
    if (data[i].order==0) {
  var url = '/api/v1/basket/'+data[i].id+'/'
  fetch(url,{
    method:'PUT',
    headers: {
      'Content-type':'application/json',
      'X-CSRFToken':getCookie('csrftoken')
    },
    body:JSON.stringify({
      'create_at':data[i].create_at,
      'modified':data[i].modified,
      'product_name':data[i].product_name,
      'product_model':data[i].product_model,
      'category':data[i].category,
      'shop_name':data[i].shop_name,   
      'order':id,
      'price':data[i].price,
      'quantity':data[i].quantity,
      'product':data[i].product,
      'shop':data[i].shop,
      'shop_products':data[i].shop_products,
      'user':data[i].user_id,
    })
  })
}
}
window.location.href = '/order_send_email/'+id;
}
function addorder(data,sum,count){
  var url = '/api/v1/orders/'
  fetch(url,{
    method:'POST',
    headers: {
      'Content-type':'application/json',
      'X-CSRFToken':getCookie('csrftoken')
    },
    body:JSON.stringify({
      'price':sum,
      'status':'basket',
      'count':count,
      'user':data[1],
    })
  }).then(response => response.json())
  .then(function(commit){
    var id = commit.id
    updatebasket(data,id)
  })}
function buildorders(){
  var wrapper = document.getElementById('tbody')
  var url = '/api/v1/orders/'
  fetch(url)
  .then((resp)=>resp.json())
  .then(function(data){
    console.log(data)
    if (data[2]=='buyer'){
      buildorders_buyer(wrapper,data)
    }
    else if (data[2]=='shop'){
      buildorders_shop(wrapper,data)
    }
    else if (data[2]=='stuff'){
      buildorders_stuff(wrapper,data)
    }
  })
}
function buildorders_buyer(wrapper,data){
  var list = data[0]
    for(var i in list){
    var item = ` 
    <tr>
      <td>${list[i].id}</td>
      <td> ${list[i].modified}</td>
      <td>${list[i].price}</td>
      <td>${list[i].status}</td>
      <td>
      <button type="button" class="btn btn-danger" id="${list[i].id}">Отменить</button></td>
        </tr>  `

wrapper.innerHTML +=item 
}
  }
  function buildorders_stuff(wrapper,data){
    var list = data[0]
      for(var i in list){
        if (list[i].user==data[1]) {
      var item = ` 
      <tr>
        <td>${list[i].id}</td>
        <td> ${list[i].modified}</td>
        <td>${list[i].price}</td>
        <td>          <select class="form-select" aria-label="Default select example">
        <option selected>${list[i].status}</option>
        <option value="1">confirmed</option>
        <option value="2">assembled</option>
        <option value="3">sent</option>
        <option value="4">delivered</option>
        <option value="5">canceled</option>
      </select></td>
        <td>
        <button type="button" class="btn btn-danger" id="${list[i].id}">Изменить</button>
        <button type="button" class="btn btn-danger" id="${list[i].id}">Отменить</button></td>
          </tr>  `
  
  wrapper.innerHTML +=item }
  }
    }
  function buildorders_shop(wrapper,data){
      var list = data[0]
        for(var i in list){
          if (list[i].user==data[1]) {
        var item = ` 
        <tr>
          <td>${list[i].id}</td>
          <td> ${list[i].modified}</td>
          <td>${list[i].price}</td>
          <td>          <select class="form-select" aria-label="Default select example">
  <option selected>${list[i].status}</option>
  <option value="1">confirmed</option>
  <option value="2">assembled</option>
  <option value="3">sent</option>
  <option value="4">delivered</option>
  <option value="5">canceled</option>
</select></td>
          <td>
          <button type="button" class="btn btn-danger" id="${list[i].id}">Изменить</button></td>
            </tr>  `
    
    wrapper.innerHTML +=item }
    }
      }
function buildbasket(){
    var wrapper = document.getElementById('tbody')
    var url = '/api/v1/basket/'
    fetch(url)
    .then((resp)=>resp.json())
    .then(function(data){
    var list = data[0]
    var count = 0
    var sum = 0
      for(var i in list){
        if (list[i].user_id==data[1] && (list[i].order==0 | list[i].order==null)) {
        count+=list[i].quantity
        sum+=list[i].price
      var item = ` 
      <tr>
        <td>${list[i].shop_name}</td>
        <td> ${list[i].product_name}</td>
        <td>${list[i].quantity}</td>
        <td>${list[i].price}</td>
        <td>
        <button type="button" class="btn btn-danger" id="${list[i].id}">Удалить</button></td>
        </tr>  `      
  wrapper.innerHTML +=item }
}
wrapper.innerHTML +=`      <tr>
<tr>
<td>#</td>
<td>ИТОГО</td>
<td>${count}</td>
<td>${sum}</td>
<td> #</td>`
      for(var i in list){
        if (list[i].user_id==data[1] && list[i].order==0) {
      var button = document.getElementById(list[i].id)  
      button.addEventListener('click',function(e){
        // если пользователя нет то перейти на страницу регистрации
        delbasket(list[i].id)
      })
    }
    }
    var confirm_basket = document.getElementById('confirm_basket') 
    if (confirm_basket != null) {
      confirm_basket.addEventListener('click',function(e){
      // если пользователя нет то перейти на страницу регистрации
      addorder(data,sum,count)
      })}
    })
    }
function buildproduct(){
    var wrapper = document.getElementById('list-product')
    var url = '/api/v1/shop/'
    fetch(url)
    .then((resp)=>resp.json())
    .then(function(data){
    var list = data[0]
    for(var i in list){
        var item = `
        <div class="col">

        <div class="card">
                      <div class="card-header text-muted">
                          ${list[i].category}
                              Магазин:   ${list[i].shop_name}
    
    
      </div>
          <div class="card-body">
            <h5 class="card-title">${list[i].product_name}</h5>
            <p class="card-text">${list[i].product_model}</p>
                      <button type="submit" class="btn btn-primary" id="${list[i].id}">В корзину</button>
          </div>
                      <div class="card-footer text-muted">
    
                          Цена:${list[i].price_rrc}
      </div>
        </div>
      </div> `
      wrapper.innerHTML +=item
    }
      for(var i in list){
      var button = document.getElementById(list[i].id)  
      button.addEventListener('click',function(e){
        if (data[1]!=null)  {
          addbasket(list[e.target.id-1],data[1])
        }
        else {
          window.location.href = '/login/'
        }
        // если пользователя нет то перейти на страницу регистрации
      })
    }
    })
    }
function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== '') {
              const cookies = document.cookie.split(';');
              for (let i = 0; i < cookies.length; i++) {
                  const cookie = cookies[i].trim();
                  // Does this cookie string begin with the name we want?
                  if (cookie.substring(0, name.length + 1) === (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }
function delbasket(data){
        var url = '/api/v1/basket/'
        fetch(url,{
          method:'DELETE',
          headers: {
            'Content-type':'application/json',
            'X-CSRFToken':getCookie('csrftoken')
          },
          body:JSON.stringify({
            'id':data,
          })
        })
        .then(function(response){
          document.getElementById('tbody').innerHTML=''
          buildbasket()
        })}
function addbasket(data,user){
      var url = '/api/v1/basket/'
      fetch(url,{
        method:'POST',
        headers: {
          'Content-type':'application/json',
          'X-CSRFToken':getCookie('csrftoken')
        },
        body:JSON.stringify({
          'quantity':1,
          'order':0,
          'product':data.product_id,
          'shop':data.shop_id,
          'shop_products':data.id,
          'user':user,
          'price':data.price_rrc
        })
      })
      .then(function(response){
        countitemsbasket()
      })}

  