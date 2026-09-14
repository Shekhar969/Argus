import StatCard from "../components/dashboard/StatCard";
import LiveCamera from "../components/dashboard/LiveCamera";
import useArgusEvents from "../hooks/useArgusEvents";


function Dashboard() {

    const {
        events,
        connected
    } = useArgusEvents();


    // Count currently active intrusions

    const activeIntrusions = events.filter(
        (event) =>
            event.event_type === "intrusion_started"
    ).length;


    return (
        <div>

            {/* ================================================= */}
            {/* PAGE HEADER */}
            {/* ================================================= */}

            <div className="mb-8">

                <p className="text-xs uppercase tracking-[0.2em] text-gray-500">
                    Overview
                </p>

                <h1 className="mt-2 text-3xl font-semibold text-white">
                    Security Dashboard
                </h1>

                <p className="mt-2 text-sm text-gray-500">
                    Real-time overview of the Argus visual intelligence system.
                </p>

            </div>


            {/* ================================================= */}
            {/* CONNECTION STATUS */}
            {/* ================================================= */}

            <div className="mb-6 flex items-center gap-2">

                <span
                    className={`h-2 w-2 rounded-full ${
                        connected
                            ? "bg-green-500"
                            : "bg-red-500"
                    }`}
                />

                <span className="text-xs text-gray-400">

                    {connected
                        ? "ARGUS ENGINE CONNECTED"
                        : "ARGUS ENGINE DISCONNECTED"
                    }

                </span>

            </div>


            {/* ================================================= */}
            {/* STATISTICS */}
            {/* ================================================= */}

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">

                <StatCard
                    title="Active Cameras"
                    value="01"
                    description="1 online"
                />

                <StatCard
                    title="Active Intrusions"
                    value={String(activeIntrusions).padStart(2, "0")}
                    description="Current session"
                />

                <StatCard
                    title="Events Today"
                    value={events.length}
                    description="Current session"
                />

                <StatCard
                    title="Objects Tracked"
                    value="—"
                    description="Live tracking"
                />

            </div>


            {/* ================================================= */}
            {/* MAIN AREA */}
            {/* ================================================= */}

            <div className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-3">


                {/* ================================================= */}
                {/* CAMERA OVERVIEW */}
                {/* ================================================= */}

                <div className="rounded-xl border border-white/10 bg-white/[0.03] p-6 xl:col-span-2">

                    <div className="flex items-center justify-between">

                        <div>

                            <h2 className="text-lg font-semibold text-white">
                                Camera Overview
                            </h2>

                            <p className="mt-1 text-xs text-gray-500">
                                Current monitoring status
                            </p>

                        </div>


                        <span className="flex items-center gap-2 rounded-md bg-green-500/10 px-3 py-1 text-xs text-green-400">

                            <span className="h-1.5 w-1.5 rounded-full bg-green-500" />

                            LIVE

                        </span>

                    </div>


                    {/* Camera grid */}

                    <div className="mt-6 grid grid-cols-2 gap-4">

                        <LiveCamera
                            cameraId="CAM-001"
                        />

                        <CameraPlaceholder
                            camera="CAM-002"
                        />

                        <CameraPlaceholder
                            camera="CAM-003"
                        />

                        <CameraPlaceholder
                            camera="CAM-004"
                        />

                    </div>

                </div>


                {/* ================================================= */}
                {/* EVENTS */}
                {/* ================================================= */}

                <div className="rounded-xl border border-white/10 bg-white/[0.03] p-6">

                    <div>

                        <h2 className="text-lg font-semibold text-white">
                            Recent Events
                        </h2>

                        <p className="mt-1 text-xs text-gray-500">
                            Latest security activity
                        </p>

                    </div>


                    <div className="mt-6 space-y-4">

                        {events.length === 0 ? (

                            <div className="rounded-lg border border-white/5 bg-black/20 p-4">

                                <p className="text-sm text-gray-400">
                                    No security events detected.
                                </p>

                                <p className="mt-1 text-xs text-gray-600">
                                    Argus is monitoring CAM-001.
                                </p>

                            </div>

                        ) : (

                            events.map((event) => (

                                <EventItem
                                    key={event.event_id}
                                    event={event}
                                />

                            ))

                        )}

                    </div>

                </div>

            </div>

        </div>
    );
}


{/* ========================================================= */}
{/* CAMERA PLACEHOLDER */}
{/* ========================================================= */}

function CameraPlaceholder({ camera }) {

    return (
        <div className="relative aspect-video overflow-hidden rounded-lg border border-white/10 bg-black">

            <div className="absolute inset-0 flex items-center justify-center">

                <span className="text-xs text-gray-600">
                    CAMERA FEED
                </span>

            </div>

            <div className="absolute bottom-0 left-0 right-0 flex items-center justify-between bg-black/70 px-3 py-2">

                <span className="text-xs text-white">
                    {camera}
                </span>

                <span className="flex items-center gap-1 text-[10px] text-green-400">

                    <span className="h-1.5 w-1.5 rounded-full bg-green-500" />

                    ONLINE

                </span>

            </div>

        </div>
    );
}


{/* ========================================================= */}
{/* EVENT ITEM */}
{/* ========================================================= */}

function EventItem({ event }) {

    const isIntrusion =
        event.event_type === "intrusion_started";


    const title =
        isIntrusion
            ? "Intrusion detected"
            : "Intrusion ended";


    const time =
        new Date(
            event.timestamp
        ).toLocaleTimeString();


    return (
        <div className="border-b border-white/5 pb-4">

            <div className="flex items-start gap-3">

                <span
                    className={`mt-1 h-2 w-2 rounded-full ${
                        isIntrusion
                            ? "bg-red-500"
                            : "bg-blue-500"
                    }`}
                />


                <div className="flex-1">

                    <p className="text-sm text-white">
                        {title}
                    </p>


                    <p className="mt-1 text-xs text-gray-500">
                        {event.camera_id}
                        {" · "}
                        {event.zone_id}
                        {" · "}
                        Track #{event.track_id}
                    </p>


                    <p className="mt-1 text-[10px] text-gray-600">
                        {time}
                    </p>

                </div>

            </div>

        </div>
    );
}


export default Dashboard;