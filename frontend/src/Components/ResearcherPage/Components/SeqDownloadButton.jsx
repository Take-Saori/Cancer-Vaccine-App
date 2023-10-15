import { Row, Col, Button, Container } from "react-bootstrap";

function SeqDownloadButton() {
    return(
    <Container className="d-flex align-items-center justify-content-center">
      <Row className="justify-content-center align-items-center">
        <Col xs="auto">
          <h5>Download: </h5>
        </Col>
        <Col xs="auto">
          <Button variant="btn btn-outline-primary">CSV</Button>
        </Col>
        <Col xs="auto">
          <Button variant="btn btn-outline-primary">Excel Sheet</Button>
        </Col>
      </Row>
    </Container>
    );
}

export default SeqDownloadButton;