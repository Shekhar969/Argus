import { useState } from "react";

import Sidebar from "./components/layout/Sidebar";
import Topbar from "./components/layout/Topbar";

import Dashboard from "./pages/Dashboard";
import Zones from "./pages/Zones";


function App() {

    const [activePage, setActivePage] =
        useState("dashboard");


    function renderPage() {

        switch (activePage) {

            case "zones":

                return <Zones />;


            case "dashboard":

            default:

                return <Dashboard />;
        }
    }


    return (
        <div className="min-h-screen bg-[#0b0d10]">

            <Sidebar
                activePage={activePage}
                setActivePage={setActivePage}
            />

            <Topbar />


            <main className="ml-64 pt-20">

                <div className="p-8">

                    {renderPage()}

                </div>

            </main>

        </div>
    );
}


export default App;