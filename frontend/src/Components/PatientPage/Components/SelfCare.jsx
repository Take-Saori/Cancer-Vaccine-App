import { Col, Container, Row } from "react-bootstrap";
import YouTubePlayer from "./YouTubePlayer";

function SelfCare() {

    // video IDs
    const videoUrls = ['r105CzDvoo0', 'BoZ0Zwab6Oc', 'ZSLmP-af8W0'];

    return(
        <Container className="py-4">
            <Row>
                <Col xs={6}>
                    <h3 style={{ textDecoration: 'underline' }}>Self Care</h3>
                    <p>A paragraph for self care.</p>
                </Col>

                <Col>
                    <YouTubePlayer videos={videoUrls} videoWidth={500} videoHeight={300} />
                </Col>
            </Row>
        </Container>
    );
}

export default SelfCare;