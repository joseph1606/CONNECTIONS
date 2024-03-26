import "./App.css";
import REPL from "./components/REPL.js";
import CSVLoader from "./components/CSV.js";

function App() {
  return <div><REPL />
    <CSVLoader />
  </div>;
}

export default App;
