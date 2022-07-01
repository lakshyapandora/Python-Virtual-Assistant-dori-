const mic = document.getElementById('mic');

const play = (e) => {
    if(mic.classList.contains('pulse')){
        mic.classList.remove('pulse');
    }else{
        mic.classList.add('pulse');
        document.getElementById('audio').play();
        setTimeout(() => {
            console.log('im here')
            eel.entry();
        },5000)
        
    }

}



eel.expose(addMessage);
function addMessage(message,type){
    
    const body = document.getElementById('body');
    
    if(type === 1){
        const incoming = document.createElement('div');
        const bubble = document.createElement('div');
        const p = document.createElement('p');
        bubble.classList.add('bubble');
        incoming.classList.add('incoming');
        bubble.append(p);
        incoming.append(bubble);
        body.append(incoming);
        typeWriter(message,p);
    }else{
        console.log('type2')
        console.log(message)
        const outgoing = document.createElement('div');
        const bubble = document.createElement('div');
        const p = document.createElement('p');
        bubble.classList.add('bubble');
        outgoing.classList.add('outgoing');
        bubble.append(p);
        outgoing.append(bubble);
        body.append(outgoing);
        typeWriter(message,p);
    }
    
}

function typeWriter(text, target){
    var speed =10;
    var i = 0;

    function inner(){
        if(i < text.length){
            target.innerHTML += text.charAt(i);
            i++;
            setTimeout(inner,speed);
        }

    }

    inner();

}