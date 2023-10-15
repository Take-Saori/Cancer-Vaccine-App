import { Container } from "react-bootstrap";

function Resources() {
    return(
        <Container className="p-4 bg-light">
            <h3 className="d-flex justify-content-center" style={{ textDecoration: 'underline' }}>Resources</h3>
            <ul className="py-4">
                <li>About this cancer</li>
                <li>Video links</li>
                <li>Self care links</li>
                <li>References</li>
            </ul>
        </Container>
    );
}

export default Resources;