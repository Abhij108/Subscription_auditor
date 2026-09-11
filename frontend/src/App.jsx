import { useState } from "react";
import UploadBox from "./components/UploadBox";
import Dashboard from "./pages/Dashboard";

function App() {

  const [data, setData] = useState(null);

  return (
    <div>

      <UploadBox
        onResult={setData}
      />

      <Dashboard
        data={data}
      />

    </div>
  );
}

export default App;