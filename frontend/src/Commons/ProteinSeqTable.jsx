import Table from 'react-bootstrap/Table';

function ProteinSeqTable() {
  return (
    <div className="p-5">
        <Table striped bordered hover >
        <thead>
            <tr>
            <th>#</th>
            <th>Protein Sequence</th>
            <th>Score</th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <td>1</td>
            <td>ABCD</td>
            <td>0.8</td>
            </tr>
            <tr>
            <td>2</td>
            <td>DEFG</td>
            <td>0.6</td>
            </tr>
            <tr>
            <td>3</td>
            <td>HIJK</td>
            <td>0.4</td>
            </tr>
        </tbody>
        </Table>
    </div>
  );
}

export default ProteinSeqTable;