if (document.getElementById('list-product')!=null){
  buildproduct()
}
if ((document.URL.match('basket'))!=null){
  buildbasket()
}
else {
  countitemsbasket()
}
function countitemsbasket() {
  var wrapper = document.getElementById('count_order')
  var url = '/api/v1/basket/'
  fetch(url)
  .then((resp)=>resp.json())
  .then(function(data){     
    var count = 0
    var list = data[0]
    for(var i in list){
        if (list[i].user_id==data[1] && list[i].status=='basket') {
          count+=1
  }}
  wrapper.textContent=count
  })
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
        if (list[i].user_id==data[1] && list[i].status=='basket') {
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
        if (list[i].user_id==data[1]) {
      var button = document.getElementById(list[i].id)  
      button.addEventListener('click',function(e){
        // если пользователя нет то перейти на страницу регистрации
        delbasket(list[i].id)
      })
    }
    }
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
        if (data[1]!=null) {
          addbasket(list[e.target.id-1],data[1])
        }
        else {
          alert('Для оформления заказа необходимо осуществить вход')
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
      console.log()
      fetch(url,{
        method:'POST',
        headers: {
          'Content-type':'application/json',
          'X-CSRFToken':getCookie('csrftoken')
        },
        body:JSON.stringify({
          'quantity':1,
          'status':'basket',
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

  