let slideindex = 1;
// let remainingtime = 70000;

// function setTime(){
// 	if(remainingtime == 0) return;
// 	let h = Math.floor(remainingtime/3600);
// 	let m = Math.floor((remainingtime%3600)/60);
// 	let s = (remainingtime%3600)%60;
// 	document.querySelector('#hours').innerHTML = h
// 	document.querySelector('#minutes').innerHTML = m
// 	document.querySelector('#seconds').innerHTML = s
//
// }
//
// setInterval(()=>{
// 	remainingtime -= 1;
// 	setTime()
// }, 1000)



function setSlide(input, index){
	slideindex = index;
	let item = document.querySelector(`#${input}`)
	let slides = [...document.querySelector('.slides').children];
	slides.forEach((element)=>{
		element.classList.remove('active')
	})
	item.classList.add('active');
}

setInterval(()=>{
	slideindex+=1;
	if(slideindex == 4){
		slideindex = 1;
	}
	setSlide(`slide${slideindex}`, slideindex)
}, 4000)


