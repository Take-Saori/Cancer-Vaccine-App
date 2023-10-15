import { Row, Col, Button, Container } from "react-bootstrap";

function InfoDownload() {
    return(
    <Container className="d-flex align-items-center justify-content-center py-4">
      <Row className="justify-content-center align-items-center">
        <Col xs="auto">
          <h5>Download Information: </h5>
        </Col>
        <Col xs="auto">
          <Button variant="btn btn-outline-primary">PDF</Button>
        </Col>
        <Col xs="auto">
          <Button variant="btn btn-outline-primary">.docx</Button>
        </Col>
      </Row>
    </Container>
    );
}

export default InfoDownload;