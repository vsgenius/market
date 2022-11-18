if (document.getElementById('list-product')!=null){
  buildproduct()
}
if ((document.URL.match('basket'))!=null){
  buildbasket()
}
if ((document.URL.match('orders'))!=null){
  buildorders()
} 
if ((document.URL.match('load_products'))!=null){
  document.getElementById('formFile_button').addEventListener('click',function(e){
    load_products()
  })
}
if ((document.URL.match('create_product'))!=null){
  document.getElementById('add').addEventListener('click',function(e){
    addproduct()
  })
}
function addproduct(){
  var url = '/api/v1/product/'
  fetch(url,{
    method:'POST',
    headers: {
      'Content-type':'application/json',
      'X-CSRFToken':getCookie('csrftoken')
    },
    body:JSON.stringify({
      'external':document.getElementById('external_id').value,
      'name':document.getElementById('name').value,
      'model':document.getElementById('model').value,
      'category':document.getElementById('category').value,
      'category_name':document.getElementById('category').value,
      'user':1,
      'items':document.getElementById('params').value
    })
  }).then(function(response){
    if (response.status==201){
      alert('Продукт добавлен')
      window.location.href='/create_product/'
    }
    else {
      alert('Ошибка при добавлении')
    }
  })}
function load_products(){
  var file_path = document.getElementById('formFile').value
  var url = '/api/v1/load_products/'
  fetch(url,{
    method:'POST',
    headers: {
      'Content-type':'application/json',
      'X-CSRFToken':getCookie('csrftoken')
    },
    body:JSON.stringify({
      'url':file_path
    })
  }).then(response => response.json())
  .then(function(commit){
    if (commit.Status==true){
      alert('Данные успешно загружены')
    }
    else {
      alert('Ошбика при загрузке данных')
    }
  })
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
                      <div class="card-header text-muted style="background-color: #e3f2fd;"">
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
              addbasket(data[0],e.target.id,data[1])
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
function addbasket(data,shopproduct_id,user){
          var url = '/api/v1/basket/'
          for (const key in data) {
            if (data[key].id==shopproduct_id) {
              var shopproduct = data[key]
            }
          }
          fetch(url,{
            method:'POST',
            headers: {
              'Content-type':'application/json',
              'X-CSRFToken':getCookie('csrftoken')
            },
            body:JSON.stringify({
              'quantity':1,
              'order':0,
              'product':shopproduct.product_id,
              'shop':shopproduct.shop_id,
              'shop_products':shopproduct.id,
              'user':user,
              'price':shopproduct.price_rrc
            })
          })
          .then(function(response){
            countitemsbasket()
          })}
$ (function($) {
  $('#form_ajax').submit(function(e){
    e.preventDefault()
    $.ajax({
    type:this.method,
    url: this.action,
    data: $(this).serialize(),
    headers: {'X-CSRFToken': getCookie('csrftoken')},
    dataType:'json',
    success:function(response){
            console.log(response)
            window.location.reload()
    },
    error:function(response){
        if (response.status===400){
          console.log(response)
            $('.alert-danger').text(response.responseJSON.error).removeClass('d-none')
          }
    }
  })
    })
    })
$ (function($) {
      $('#form_ajax').submit(function(e){
        console.log(this)
        e.preventDefault()
        $.ajax({
        type:this.method,
        url: this.action,
        data: $(this).serialize(),
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        dataType:'json',
        success:function(response){
                console.log(response)
                window.location.reload()
        },
        error:function(response){
          console.log(response)
            if (response.status===400){
              console.log(response)
                $('.alert-danger').text(response.responseJSON.error).removeClass('d-none')
              }
        }
      })
        })
        })
$ (function($) {
          $('#form_create_product').submit(function(e){
            console.log(this) 
            e.preventDefault()
            $.ajax({
            type:this.method,
            url: this.action,
            data: $(this).serialize(),
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            dataType:'json',
            success:function(response){
                    console.log(response)
                    window.location.reload()
            },
            error:function(response){
              console.log(response)
                if (response.status===400){
                  console.log(response)
                    $('.alert-danger').text(response.responseJSON.error).removeClass('d-none')
                  }
            }
          })
            })
            })
  