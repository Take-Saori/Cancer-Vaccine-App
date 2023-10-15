import { Tab, Tabs } from 'react-bootstrap';
import ProteinSeqTable from '../../../Commons/ProteinSeqTable';
import SeqDownloadButton from './SeqDownloadButton';
import AboutCancer from '../../PatientPage/Components/AboutCancer';
import SelfCare from '../../PatientPage/Components/SelfCare';
import Resources from '../../PatientPage/Components/Resources';
import InfoDownload from '../../PatientPage/Components/InfoDownload';

function ViewTab() {
  return (
    <Tabs
      defaultActiveKey="researcherView"
      id="justify-tab-example"
      className="mb-3"
      justify
    >
      <Tab eventKey="researcherView" title="Researcher View">
        <div className="text-center">
          <h3 className="py-4"
              style={{ textDecoration: 'underline' }}>
          Consolidated possible protein binding
          </h3>
        </div>
        <SeqDownloadButton />
        <ProteinSeqTable />
      </Tab>

      <Tab eventKey="patientView" title="Patient View">
        <AboutCancer />
        <SelfCare />
        <Resources />
        <InfoDownload />
      </Tab>
    </Tabs>
  );
}

export default ViewTab;