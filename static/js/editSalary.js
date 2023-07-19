

len = document.querySelectorAll('.updateButton').length

for(let i=0; i<len; i++){
    
    document.querySelectorAll('.updateButton')[i].addEventListener('click', function(){
        
        let salary = document.querySelectorAll('.updateSalary')[i].innerText;
        document.querySelectorAll('.updateSalary')[i].innerHTML = 
        `<input type='text' value='${ salary }' name='salary' style="width:100px">`;
    
        document.querySelectorAll('.updateButton')[i].innerHTML = 
        `update`

        document.querySelectorAll('.updateSalary')[i].parentElement.querySelector("input[type=submit]").style.display = 'inline'

    })

}


