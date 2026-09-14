import { useEffect, useRef, useState } from "react";


function ZoneEditor() {

    const containerRef = useRef(null);
    const canvasRef = useRef(null);

    const [points, setPoints] = useState([]);

    const [isSelecting, setIsSelecting] =
        useState(false);

    const [saving, setSaving] =
        useState(false);

    const [message, setMessage] =
        useState("");


    const cameraId = "CAM-001";

    const streamUrl =
        "http://127.0.0.1:8000/api/camera/stream";


    // ========================================================
    // DRAW ZONE
    // ========================================================

    useEffect(() => {

        const canvas =
            canvasRef.current;

        const container =
            containerRef.current;

        if (!canvas || !container) {
            return;
        }


        const width =
            container.clientWidth;

        const height =
            width * 9 / 16;


        canvas.width = width;
        canvas.height = height;


        const ctx =
            canvas.getContext("2d");


        ctx.clearRect(
            0,
            0,
            width,
            height
        );


        if (points.length === 0) {
            return;
        }


        // ----------------------------------------------------
        // Connecting lines
        // ----------------------------------------------------

        ctx.beginPath();

        points.forEach(
            (point, index) => {

                if (index === 0) {

                    ctx.moveTo(
                        point.x,
                        point.y
                    );

                } else {

                    ctx.lineTo(
                        point.x,
                        point.y
                    );
                }
            }
        );


        ctx.strokeStyle =
            "#22c55e";

        ctx.lineWidth = 2;

        ctx.stroke();


        // ----------------------------------------------------
        // Close polygon preview
        // ----------------------------------------------------

        if (points.length >= 3) {

            ctx.beginPath();

            ctx.moveTo(
                points[points.length - 1].x,
                points[points.length - 1].y
            );

            ctx.lineTo(
                points[0].x,
                points[0].y
            );

            ctx.strokeStyle =
                "#3b82f6";

            ctx.lineWidth = 2;

            ctx.stroke();


            // ------------------------------------------------
            // Polygon fill
            // ------------------------------------------------

            ctx.beginPath();

            points.forEach(
                (point, index) => {

                    if (index === 0) {

                        ctx.moveTo(
                            point.x,
                            point.y
                        );

                    } else {

                        ctx.lineTo(
                            point.x,
                            point.y
                        );
                    }
                }
            );

            ctx.closePath();

            ctx.fillStyle =
                "rgba(59, 130, 246, 0.15)";

            ctx.fill();
        }


        // ----------------------------------------------------
        // Draw numbered points
        // ----------------------------------------------------

        points.forEach(
            (point, index) => {

                // Point

                ctx.beginPath();

                ctx.arc(
                    point.x,
                    point.y,
                    6,
                    0,
                    Math.PI * 2
                );

                ctx.fillStyle =
                    "#ef4444";

                ctx.fill();


                // White outline

                ctx.strokeStyle =
                    "#ffffff";

                ctx.lineWidth = 2;

                ctx.stroke();


                // Number

                ctx.font =
                    "600 14px Arial";

                ctx.fillStyle =
                    "#ffffff";

                ctx.fillText(
                    String(index + 1),
                    point.x + 10,
                    point.y - 10
                );
            }
        );

    }, [points]);


    // ========================================================
    // HANDLE CLICK
    // ========================================================

    function handleCanvasClick(event) {

        if (!isSelecting) {
            return;
        }


        const canvas =
            canvasRef.current;

        if (!canvas) {
            return;
        }


        const rect =
            canvas.getBoundingClientRect();


        const scaleX =
            canvas.width /
            rect.width;

        const scaleY =
            canvas.height /
            rect.height;


        const x =
            (event.clientX - rect.left) *
            scaleX;

        const y =
            (event.clientY - rect.top) *
            scaleY;


        setPoints(
            previous => [
                ...previous,
                {
                    x,
                    y
                }
            ]
        );


        setMessage("");
    }


    // ========================================================
    // START SELECTION
    // ========================================================

    function startSelection() {

        setPoints([]);

        setMessage("");

        setIsSelecting(true);
    }


    // ========================================================
    // RESET
    // ========================================================

    function resetSelection() {

        setPoints([]);

        setMessage("");
    }


    // ========================================================
    // CANCEL
    // ========================================================

    function cancelSelection() {

        setPoints([]);

        setIsSelecting(false);

        setMessage(
            "Zone selection cancelled."
        );
    }


    // ========================================================
    // CONFIRM / SAVE
    // ========================================================

    async function confirmZone() {

        if (points.length < 3) {

            setMessage(
                "A zone requires at least 3 points."
            );

            return;
        }


        setSaving(true);

        setMessage(
            "Saving zone..."
        );


        try {

            const canvas =
                canvasRef.current;


            // ------------------------------------------------
            // Current displayed canvas dimensions
            // ------------------------------------------------

            const displayWidth =
                canvas.clientWidth;

            const displayHeight =
                canvas.clientHeight;


            // ------------------------------------------------
            // Backend camera frame dimensions
            //
            // Your current camera stream is treated as
            // 1920 × 1080 for coordinate conversion.
            // ------------------------------------------------

            const cameraWidth =
                1920;

            const cameraHeight =
                1080;


            // ------------------------------------------------
            // Convert frontend coordinates to camera coords
            // ------------------------------------------------

            const coordinates =
                points.map(
                    point => ({

                        x: Math.round(
                            point.x /
                            displayWidth *
                            cameraWidth
                        ),

                        y: Math.round(
                            point.y /
                            displayHeight *
                            cameraHeight
                        )

                    })
                );


            // ------------------------------------------------
            // Send to backend
            // ------------------------------------------------

            const response =
                await fetch(
                    "http://127.0.0.1:8000/api/zones",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                zone_id:
                                    "ZONE-01",

                                camera_id:
                                    cameraId,

                                coordinates:
                                    coordinates

                            })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `HTTP ${response.status}`
                );
            }


            const data =
                await response.json();


            console.log(
                "Zone saved:",
                data
            );


            setIsSelecting(false);

            setMessage(
                "Zone confirmed successfully."
            );


        } catch (error) {

            console.error(
                "Zone save failed:",
                error
            );

            setMessage(
                "Failed to save zone."
            );

        } finally {

            setSaving(false);
        }
    }


    return (

        <div className="space-y-6">


            {/* =================================================
                CAMERA / ZONE CANVAS
            ================================================= */}

            <div
                ref={containerRef}
                className="relative overflow-hidden rounded-xl border border-white/10 bg-black"
            >

                {/* Camera */}

                <img
                    src={streamUrl}
                    alt={`${cameraId} zone configuration`}
                    className="block aspect-video w-full object-cover"
                />


                {/* Drawing Canvas */}

                <canvas
                    ref={canvasRef}
                    onClick={handleCanvasClick}
                    className={`absolute left-0 top-0 h-full w-full ${
                        isSelecting
                            ? "cursor-crosshair"
                            : "pointer-events-none"
                    }`}
                />


                {/* Camera label */}

                <div className="absolute left-4 top-4 rounded-md bg-black/70 px-3 py-2 backdrop-blur">

                    <p className="text-xs font-medium text-white">
                        {cameraId}
                    </p>

                    <p className="text-[10px] uppercase tracking-wider text-gray-500">
                        Zone Configuration
                    </p>

                </div>


                {/* Selection status */}

                {isSelecting && (

                    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 rounded-md bg-black/80 px-4 py-2 text-xs text-white backdrop-blur">

                        Click points to create the zone

                    </div>

                )}

            </div>


            {/* =================================================
                CONTROLS
            ================================================= */}

            <div className="flex items-center justify-between rounded-xl border border-white/10 bg-[#111418] p-4">


                {/* Instructions */}

                <div>

                    <p className="text-sm font-medium text-white">
                        Restricted Zone
                    </p>

                    <p className="mt-1 text-xs text-gray-500">

                        {points.length === 0
                            ? "No points selected."
                            : `${points.length} point${points.length === 1 ? "" : "s"} selected.`
                        }

                    </p>

                </div>


                {/* Buttons */}

                <div className="flex items-center gap-2">


                    {!isSelecting && (

                        <button
                            type="button"
                            onClick={startSelection}
                            className="rounded-lg bg-white/10 px-4 py-2 text-sm font-medium text-white transition hover:bg-white/20"
                        >
                            Select Zone
                        </button>

                    )}


                    {isSelecting && (

                        <>

                            <button
                                type="button"
                                onClick={resetSelection}
                                className="rounded-lg bg-white/10 px-4 py-2 text-sm font-medium text-gray-300 transition hover:bg-white/20"
                            >
                                Reset
                            </button>


                            <button
                                type="button"
                                onClick={cancelSelection}
                                className="rounded-lg bg-white/10 px-4 py-2 text-sm font-medium text-gray-300 transition hover:bg-white/20"
                            >
                                Cancel
                            </button>


                            <button
                                type="button"
                                onClick={confirmZone}
                                disabled={
                                    saving ||
                                    points.length < 3
                                }
                                className="rounded-lg bg-red-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-600 disabled:cursor-not-allowed disabled:opacity-40"
                            >
                                {saving
                                    ? "Saving..."
                                    : "Confirm Zone"
                                }
                            </button>

                        </>

                    )}

                </div>

            </div>


            {/* =================================================
                MESSAGE
            ================================================= */}

            {message && (

                <div className="rounded-lg border border-white/10 bg-[#111418] px-4 py-3 text-sm text-gray-300">

                    {message}

                </div>

            )}

        </div>
    );
}


export default ZoneEditor;