import { Swiper, SwiperSlide } from 'swiper/react'
import { Navigation } from 'swiper';
import 'swiper/css'
import slide_img from '../img/Rectangle 27.png'
import 'swiper/css/navigation';
import 'swiper/css/pagination';


function Music() {
    return (
        <>
            <section class="music">
                <div class="container">
                    <Swiper
                        modules={[Navigation]}
                        spaceBetween={50}
                        slidesPerView={3}
                        navigation
                    >
                        <SwiperSlide>
                            <div class="card-music">
                                <img src={slide_img} alt=""/>
                                <h2 class="music-title">
                                    Chandler, AZ
                                </h2>
                                <p class="music-text">
                                    The Park at Wild Horse Pass
                                </p>
                                <div class="music-aside flex">
                                    <p class="music-date">
                                        Apr 02 2021
                                    </p>
                                    <a class="music-listen-link" href="">
                                        <button class="music-listen-button">
                                            LISTEN
                                        </button>
                                    </a>
                                </div>
                            </div>
                        </SwiperSlide>
                        <SwiperSlide>
                            <div class="card-music">
                                <img src={slide_img}  alt=""/>
                                <h2 class="music-title">
                                    Chandler, AZ
                                </h2>
                                <p class="music-text">
                                    The Park at Wild Horse Pass
                                </p>
                                <div class="music-aside flex">
                                    <p class="music-date">
                                        Apr 02 2021
                                    </p>
                                    <a class="music-listen-link" href="">
                                        <button class="music-listen-button">
                                            LISTEN
                                        </button>
                                    </a>
                                </div>
                            </div>
                        </SwiperSlide>
                        <SwiperSlide>
                            <div class="card-music">
                                <img src={slide_img}  alt=""/>
                                <h2 class="music-title">
                                    Chandler, AZ
                                </h2>
                                <p class="music-text">
                                    The Park at Wild Horse Pass
                                </p>
                                <div class="music-aside flex">
                                    <p class="music-date">
                                        Apr 02 2021
                                    </p>
                                    <a class="music-listen-link" href="">
                                        <button class="music-listen-button">
                                            LISTEN
                                        </button>
                                    </a>
                                </div>
                            </div>
                        </SwiperSlide>
                        <SwiperSlide>
                            <div class="card-music">
                                <img src={slide_img}  alt=""/>
                                <h2 class="music-title">
                                    Chandler, AZ
                                </h2>
                                <p class="music-text">
                                    The Park at Wild Horse Pass
                                </p>
                                <div class="music-aside flex">
                                    <p class="music-date">
                                        Apr 02 2021
                                    </p>
                                    <a class="music-listen-link" href="">
                                        <button class="music-listen-button">
                                            LISTEN
                                        </button>
                                    </a>
                                </div>
                            </div>
                        </SwiperSlide>
                        <SwiperSlide>
                            <div class="card-music">
                                <img src={slide_img}  alt=""/>
                                <h2 class="music-title">
                                    Chandler, AZ
                                </h2>
                                <p class="music-text">
                                    The Park at Wild Horse Pass
                                </p>
                                <div class="music-aside flex">
                                    <p class="music-date">
                                        Apr 02 2021
                                    </p>
                                    <a class="music-listen-link" href="">
                                        <button class="music-listen-button">
                                            LISTEN
                                        </button>
                                    </a>
                                </div>
                            </div>
                        </SwiperSlide>
                    </Swiper>
                </div>
            </section>
        </>
    )
}

export default Music