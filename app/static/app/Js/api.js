
	
window.addEventListener('load', () => {

    let lon
    let lat 

    let temperaturaValor = document.getElementById('temperatura-valor')
    let temperaturaDescripcion = document.getElementById('temperatura-descripcion')
    let ubicacion = document.getElementById('ubicacion')
    let iconoAnimado = document.getElementById('icono-animado')
    let vientoVelocidad = document.getElementById('viento-velocidad')

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition( posicion => {
    lon = posicion.coords.longitude
    lat = posicion.coords.latitude
    //const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=303501d30780439a05d0b2ce987ee97f`
    //console.log(url)

    // Me costo mucho esto
    const url = `https://api.openweathermap.org/data/2.5/weather?q=Santiago&lang=es&units=metric&appid=303501d30780439a05d0b2ce987ee97f`

    fetch(url)
    .then(response => { return response.json()  })
    .then(data => {
    let temp = Math.round(data.main.temp)
    temperaturaValor.textContent=`${temp} °C`
    let desc = data.weather[0].description
    temperaturaDescripcion.textContent = desc.toUpperCase()
    ubicacion.textContent = data.name
    vientoVelocidad.textContent = `${data.wind.speed} m/s`
    
    //console.log(data.wind.speed)
// iconos estaticos 
    // console.log(data.weather[0].icon)
    // let iconCode = data.weather[0].icon
    // const urlIcon = `http://openweathermap.org/img/wn/${iconCode}.png`
    // console.log(urlIcon)

    console.log(data.weather[0].main)
    switch (data.weather[0].main) {
        case 'Thunderstorm':
            iconoAnimado.src="{% static 'app/animated/thunder.svg' %}"
            console.log('TORMENTA');
            break;
    case 'Drizzle':
    iconoAnimado.src="{% static 'app/animated/rainy-2.svg' %}"
    console.log('LLOVIZNA');
    break;
    case 'Rain':
    iconoAnimado.src="{% static 'app/animated/rainy-7.svg' %}"
    console.log('LLUVIA');
    break;
    case 'Snow':
    iconoAnimado.src="{% static 'app/animated/snowy-6.svg' %}"
        console.log('NIEVE');
    break;                        
    case 'Clear':
        iconoAnimado.src="{% static 'app/animated/day.svg'}"
        console.log('LIMPIO');
    break;
    case 'Atmosphere':
    iconoAnimado.src="{% static 'app/animated/weather.svg' %}"
        console.log('ATMOSFERA');
        break;  
    case 'Clouds':
        iconoAnimado.src="{% static 'app/animated/cloudy-day-1.svg' %}"
        console.log('NUBES');
        break;  
    default:
    iconoAnimado.src="{% static 'app/animated/cloudy-day-1.svg' %}"
    console.log('por defecto');

    }


    
    })
    .catch(error => {
    console.log(error)
        })

    })
    }
})