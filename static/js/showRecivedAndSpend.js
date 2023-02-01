
document.querySelector('#filterByName').style.display = 'none';
document.querySelector('#filterByDate').style.display = 'none';
document.querySelector('#filterByBoth').style.display = 'none';
document.querySelector('.recivedAccount').style.display = "inline-block";


document.querySelector('#changeVisibility').addEventListener('click', function(){

    if (document.querySelector('.spendAccount').style.display=='inline-block'){
        document.querySelector('.spendAccount').style.display = 'none';
        document.querySelector('.recivedAccount').style.display = 'inline-block';
        document.querySelector('#changeVisibility').innerText = 'Spend Money'
        
    }else if (document.querySelector('.recivedAccount').style.display == 'inline-block'){
        document.querySelector('.recivedAccount').style.display = 'none';
        document.querySelector('.spendAccount').style.display = 'inline-block';
        document.querySelector('#changeVisibility').innerText = 'Recived Money';
        
    }else{
        console.log("Something is wrong");
    }
    
    
})






document.querySelector('#applyFilterByDate').addEventListener('click',function(){
    document.querySelector("#startDate").value = '2000-01-01';
    document.querySelector('#filterByName').style.display = 'none'
    document.querySelector('#filterByBoth').style.display = 'none';
    document.querySelector('#filterByDate').style.display = 'inline-block'
})



document.querySelector('#applyFilterByName').addEventListener('click',function(){
    document.querySelector('#filterByName').style.display = 'inline-block'
    document.querySelector('#filterByBoth').style.display = 'none';
    document.querySelector('#filterByDate').style.display = 'none'
})


document.querySelector('#applyFilterByBoth').addEventListener('click',function(){
    document.querySelector('#filterByName').style.display = 'none';
    document.querySelector('#filterByDate').style.display = 'none';
    document.querySelector('#filterByBoth').style.display = 'inline-block';
})