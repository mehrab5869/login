let name_inp = document.querySelector('.inp_name')

let btn = document.querySelector('.submit')

let box = document.querySelector('.box')

let alert_1 = document.querySelector('.alert')

let text_alert = document.querySelector('.text_alert')


btn.addEventListener('click' , function(){
    
    if(name_inp.value == 'ali'|| name_inp.value == 'reza'){
        alert_1.classList.add('alert_success')
        text_alert.innerHTML = 'dorost'
        setTimeout(function(){
            alert_1.classList.remove('alert_success')
            text_alert.innerHTML = ''
        } , 3000)
    }else{
        alert_1.classList.add('alert_danger')
        text_alert.innerHTML = 'eshtebah'
        setTimeout(function(){
            alert_1.classList.remove('alert_danger')
            text_alert.innerHTML = ''
        } , 3000)
    }
})


