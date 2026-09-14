import { useEffect, useState } from "react";
import ZoneEditor from "../components/dashboard/zone/ZoneEditor";


function Zones() {

    const cameraId = "CAM-001";

    const [savedZone, setSavedZone] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);


    // ========================================================
    // LOAD SAVED ZONE
    // ========================================================

    useEffect(() => {

        async function loadZone() {

            try {

                setLoading(true);

                setError(null);


                const response = await fetch(
                    `http://127.0.0.1:8000/api/zones/camera/${cameraId}`
                );


                // ------------------------------------------------
                // No zone configured
                // ------------------------------------------------

                if (response.status === 404) {

                    setSavedZone(null);

                    return;
                }


                if (!response.ok) {

                    throw new Error(
                        "Failed to load zone."
                    );
                }


                const data = await response.json();


                setSavedZone(
                    data.zone
                );

            }
            catch (error) {

                console.error(
                    "Failed to load zone:",
                    error
                );

                setError(
                    "Could not load saved zone."
                );

            }
            finally {

                setLoading(false);

            }
        }


        loadZone();

    }, []);


    // ========================================================
    // LOADING
    // ========================================================

    if (loading) {

        return (
            <div className="p-8 text-sm text-gray-400">
                Loading zone...
            </div>
        );
    }


    // ========================================================
    // PAGE
    // ========================================================

    return (

        <div className="p-8">

            {/* Header */}

            <div className="mb-6">

                <h1 className="text-xl font-semibold text-white">
                    Zones
                </h1>

                <p className="mt-1 text-sm text-gray-500">
                    Configure restricted zones for camera {cameraId}
                </p>

            </div>


            {/* Error */}

            {error && (

                <div className="mb-4 rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">

                    {error}

                </div>

            )}


            {/* Zone Editor */}

            <ZoneEditor
                cameraId={cameraId}
                savedZone={savedZone}
            />

        </div>
    );
}


export default Zones;