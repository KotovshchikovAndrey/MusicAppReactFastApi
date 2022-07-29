import '../css/normalize.css'
import '../css/style.css'
import logo from '../img/Group 26.svg'
import slogan from '../img/War For Love.svg'
import header_music from '../img/KILLKA.mp3'


function Header() {
  return (
    <>
      <header class="header">
        <nav class="header-nav">
          <ul class="header-nav-list container flex">
            <img class="header-logo" src={logo} alt="logo"/> 
            <li class="header-nav-item"><a class="header-nav-link" href="">About</a></li>
            <li class="header-nav-item"><a class="header-nav-link" href="">News</a></li>
            <li class="header-nav-item"><a class="header-nav-link" href="">Music</a></li>
            <li class="header-nav-item"><a class="header-nav-link" href="">Media</a></li>
            <li class="header-nav-item"><a class="header-nav-link" href="">Tours</a></li>
            <li class="header-nav-item"><a class="header-nav-link" href="">Contacts</a></li>
          </ul>
        </nav>
        <div class="header-slogan-aside container">
          <h2 class="header-slogan-one">New Single</h2>
          <img class="header-slogan-two" src={slogan} alt="slogan"/>
        </div>
        <div class="header-audio-aside container">
          <audio controls class="header-audio">
            <source src={header_music} type="audio/ogg; codecs=vorbis"/>
            <source src={header_music} type="audio/mpeg"/>
            Тег audio не поддерживается вашим браузером. 
          </audio>
        </div>
      </header>
    </>
  )
}

export default Header