import last_track_img_1 from '../img/Group 10.png'
import last_track_img_2 from '../img/Group 31.svg'
import last_track from '../img/KILLKA.mp3'


function LastTracks() {
    return (
        <>
            <section class="last-tracks">
                <div class="container flex last-tracks-container">
                    <img class="last-tracks-img" src={last_track_img_1} alt=""/>
                    <div class="last-tracks-wrapper flex">
                        <div class="last-tracks-header-aside flex">
                            <img class="last-tracks-header-img" src={last_track_img_2} alt=""/>
                            <h2 class="last-tracks-title">
                                Last tracks
                            </h2>
                        </div>
                        <ul class="last-audio-list">
                            <li class="last-audio-item">
                                <p class="audio-title">3LAU, Bright Lights — How You Love Me</p>
                                <audio controls class="last-tracks-audio">
                                    <source src={last_track} type="audio/ogg; codecs=vorbis"/>
                                    <source src={last_track} type="audio/mpeg"/>
                                    Тег audio не поддерживается вашим браузером. 
                                </audio>
                            </li>
                            <li class="last-audio-item">
                                <p class="audio-title">3LAU, Bright Lights — How You Love Me</p>
                                <audio controls class="last-tracks-audio">
                                    <source src={last_track} type="audio/ogg; codecs=vorbis"/>
                                    <source src={last_track} type="audio/mpeg"/>
                                    Тег audio не поддерживается вашим браузером. 
                                </audio>
                            </li>
                            <li class="last-audio-item">
                                <p class="audio-title">3LAU, Bright Lights — How You Love Me</p>
                                <audio controls class="last-tracks-audio">
                                    <source src={last_track} type="audio/ogg; codecs=vorbis"/>
                                    <source src={last_track} type="audio/mpeg"/>
                                    Тег audio не поддерживается вашим браузером. 
                                </audio>
                            </li>
                        </ul>
                    </div>
                </div>
            </section>
        </>
    )
}

export default LastTracks