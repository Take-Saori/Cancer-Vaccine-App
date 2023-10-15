import { Navbar } from 'react-bootstrap';

function TopHeader() {
  return (
    <Navbar className="navbar navbar-expand-lg bg-primary" data-bs-theme="dark">
      <div className="container-fluid">
        <a className="navbar-brand" href="#">Cancer Vaccine Info</a>
      </div>
    </Navbar>
  );
}

export default TopHeader;