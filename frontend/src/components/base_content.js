import header_news_img_1 from '../img/Rectangle 7.png'
import header_news_img_2 from '../img/Rectangle 10.png'
import header_news_img_3 from '../img/Rectangle 71.png'
import header_news_img_4 from '../img/Rectangle 72.png'
import main_mirits_img_1 from '../img/Group 31.svg'
import main_mirits_img_2 from '../img/Rectangle 12.svg'
import main_mirits_img_3 from '../img/Rectangle 16.png'
import main_mirits_img_4 from '../img/Rectangle 17.png'
import Music from './music'
import LastTracks from './last_tracks'


function Base() {
    return (
        <>
            <section class="news-section">
                <div class="flex container news-section-container">
                    <div class="header-news-wrapper">
                        <img class="header-news-img" src={header_news_img_1} alt=""/>
                        <div class="header-news-img-wrapper">
                            <img class="header-news-img" src={header_news_img_2} alt=""/>
                            <p class="header-news-text">
                                Working on my upcoming full-lenth
                                album that`s releasing later this year.
                            </p>
                        </div>
                    </div>
                    <div class="header-news-wrapper">
                        <img class="header-news-img" src={header_news_img_3} alt=""/>
                        <div class="header-news-img-wrapper">
                            <img class="header-news-img" src={header_news_img_2} alt=""/>
                            <p class="header-news-text">
                                Halloween vibes. <br/>
                                Listen my new track!
                            </p>
                        </div>
                    </div>
                    <div class="header-news-wrapper">
                        <img class="header-news-img" src={header_news_img_4} alt=""/> 
                        <div class="header-news-img-wrapper">
                            <img class="header-news-img" src={header_news_img_2} alt=""/>
                            <p class="header-news-text">
                                WarForLove is OUT NOW!! <br/> 
                                Stream it here!
                            </p>
                        </div>
                    </div>
                </div>
            </section>
            <section class="merits">
                <div class="container">
                    <div class="merits-container flex">
                        <div class="merits-text-wrapper">
                            <div class="merits-text-aside flex">
                                <img class="merits-text-img" src={main_mirits_img_1} alt=""/>
                                <h2 class="merits-header">
                                    Bright Lights
                                </h2>
                            </div>
                            <p class="merits-text">
                                Bright Lights is a multi-Grammy nominated singer, songwriter, DJ and record producer. 
                                She has written for numerous pop stars including Britney Spears, Justin Bieber, 
                                Usher and Beyoncé. Her catalog has amassed over 1 billion streams worldwide. 
                                More than 100 million of those streams can be attributed to her artist career and include such hits as 
                                Porter Robinson's "Language," 3LAU's "How You Love Me" and her own single "Runaway." She was also a 
                                featured vocalist on Zedd's #1 Clarity album. Her latest music video, "Put It Down," reached 1 million 
                                streams in the first week, releasing independently. Bright Lights is currently in the studio working on a 
                                self-produced album slated for release in 2020. 
                            </p>
                            <div class="merits-icon-wrapper flex">
                                <div class="merits-icon flex">
                                    <img class="merits-icon-img" src={main_mirits_img_2} alt=""/>
                                    <p class="merits-icon-text">Based in: Los Angeles</p>
                                </div>
                                <div class="merits-icon flex">
                                    <img class="merits-icon-img" src={main_mirits_img_2} alt=""/>
                                    <p class="merits-icon-text">Founded in 2011</p>
                                </div>
                                <div class="merits-icon flex">
                                    <img class="merits-icon-img" src={main_mirits_img_2} alt=""/>
                                    <p class="merits-icon-text">Genre: #DancePop</p>
                                </div>
                                <div class="merits-icon flex">
                                    <img class="merits-icon-img" src={main_mirits_img_2} alt=""/>
                                    <p class="merits-icon-text">Label: 333 Recordings</p>
                                </div>
                            </div>
                        </div>
                        <div class="merits-img">
                            <img class="merits-img-top" src={main_mirits_img_3} alt=""/>
                            <img class="merits-img-bottom" src={main_mirits_img_4} alt=""/>
                        </div>
                    </div>
                </div>
            </section>
        </>
    )
  }
  
  export default Base