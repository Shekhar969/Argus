function Sidebar({
    activePage,
    setActivePage
}) {

    return (
        <aside className="fixed left-0 top-0 h-screen w-64 border-r border-white/10 bg-[#0b0d10]">

            {/* Logo */}

            <div className="flex h-20 items-center border-b border-white/10 px-6">

                <div>

                    <h1 className="text-xl font-bold tracking-[0.25em] text-white">
                        ARGUS
                    </h1>

                    <p className="mt-1 text-[10px] uppercase tracking-[0.2em] text-gray-500">
                        Visual Intelligence
                    </p>

                </div>

            </div>


            {/* Navigation */}

            <nav className="px-3 py-6">


                {/* Monitoring */}

                <p className="px-3 pb-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-gray-500">
                    Monitoring
                </p>


                <SidebarItem
                    label="Dashboard"
                    active={
                        activePage === "dashboard"
                    }
                    onClick={() =>
                        setActivePage("dashboard")
                    }
                />


                <SidebarItem
                    label="Live Monitoring"
                    active={
                        activePage === "live"
                    }
                    onClick={() =>
                        setActivePage("live")
                    }
                />


                <SidebarItem
                    label="Cameras"
                    active={
                        activePage === "cameras"
                    }
                    onClick={() =>
                        setActivePage("cameras")
                    }
                />


                <SidebarItem
                    label="Zones"
                    active={
                        activePage === "zones"
                    }
                    onClick={() =>
                        setActivePage("zones")
                    }
                />


                {/* Intelligence */}

                <p className="px-3 pb-3 pt-8 text-[10px] font-semibold uppercase tracking-[0.2em] text-gray-500">
                    Intelligence
                </p>


                <SidebarItem
                    label="Events"
                    active={
                        activePage === "events"
                    }
                    onClick={() =>
                        setActivePage("events")
                    }
                />


                <SidebarItem
                    label="Evidence"
                    active={
                        activePage === "evidence"
                    }
                    onClick={() =>
                        setActivePage("evidence")
                    }
                />


                <SidebarItem
                    label="People"
                    active={
                        activePage === "people"
                    }
                    onClick={() =>
                        setActivePage("people")
                    }
                />


                <SidebarItem
                    label="Vehicles"
                    active={
                        activePage === "vehicles"
                    }
                    onClick={() =>
                        setActivePage("vehicles")
                    }
                />


                {/* System */}

                <p className="px-3 pb-3 pt-8 text-[10px] font-semibold uppercase tracking-[0.2em] text-gray-500">
                    System
                </p>


                <SidebarItem
                    label="Settings"
                    active={
                        activePage === "settings"
                    }
                    onClick={() =>
                        setActivePage("settings")
                    }
                />

            </nav>

        </aside>
    );
}


function SidebarItem({
    label,
    active = false,
    onClick
}) {

    return (
        <button
            type="button"
            onClick={onClick}
            className={`mb-1 w-full rounded-lg px-3 py-2.5 text-left text-sm transition ${
                active
                    ? "bg-white/10 text-white"
                    : "text-gray-400 hover:bg-white/5 hover:text-white"
            }`}
        >

            {label}

        </button>
    );
}


export default Sidebar;