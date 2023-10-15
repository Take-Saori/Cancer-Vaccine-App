import { useState } from 'react';
import { Dropdown, Button, Form, Container, Row, Col } from 'react-bootstrap';

function SearchBar() {

    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
    };

    return (
            <Container fluid className="p-5 bg-light" >
                <Row>
                    <Col className="d-flex align-items-center justify-content-end">
                        <Dropdown className="mr-3">
                        <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                            Cancer Type
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item >Action</Dropdown.Item>
                            <Dropdown.Item >Another action</Dropdown.Item>
                            <Dropdown.Item >Something else here</Dropdown.Item>
                        </Dropdown.Menu>
                        </Dropdown>
                    </Col>

                    <Col xs={6} className="d-flex">
                        <Form.Group className="input-group">
                            <input
                                type="text"
                                className="form-control"
                                readOnly
                                value={selectedFile ? selectedFile.name : 'Upload Sequence (.xlsl file) here'}
                                />
                            <label className="input-group-btn">
                            <span className="btn btn-primary">
                                Upload File
                                <input
                                type="file"
                                style={{ display: 'none' }}
                                onChange={handleFileUpload}
                                />
                            </span>
                            </label>
                        </Form.Group>
                    </Col>

                    <Col>
                        <Button variant="primary" className="ml-2">
                            Search
                        </Button>
                    </Col>
            </Row>
        </Container>
            
  );
}

export default SearchBar;
