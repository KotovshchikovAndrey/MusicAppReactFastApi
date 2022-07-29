import Header from "../components/header"
import Base from '../components/base_content'
import LastTracks from '../components/last_tracks'
import Music from "../components/music"


function MainPage() {
    return (
        <>
            <Header/>
            <main class="main">
                <Base/>
                <LastTracks/>
                <Music/>
            </main>
        </>
    )
}

export default MainPage