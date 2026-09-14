function LiveCamera({ cameraId }) {

    const streamUrl =
        "http://127.0.0.1:8000/api/camera/stream";

    return (
        <div className="relative overflow-hidden rounded-xl border border-white/10 bg-black">

            {/* Live Video */}

            <img
                src={streamUrl}
                alt={`${cameraId} live feed`}
                className="block aspect-video w-full object-cover"
            />


            {/* LIVE Indicator */}

            <div className="absolute left-4 top-4 flex items-center gap-2 rounded-md bg-black/70 px-3 py-2 backdrop-blur">

                <span className="h-2 w-2 animate-pulse rounded-full bg-red-500" />

                <span className="text-xs font-medium text-white">
                    LIVE
                </span>

            </div>


            {/* Camera Information */}

            <div className="absolute bottom-0 left-0 right-0 flex items-center justify-between bg-black/75 px-4 py-3 backdrop-blur">

                <div>

                    <p className="text-sm font-medium text-white">
                        {cameraId}
                    </p>

                    <p className="text-[10px] uppercase tracking-wider text-gray-500">
                        Argus Camera Feed
                    </p>

                </div>


                <div className="flex items-center gap-2">

                    <span className="h-1.5 w-1.5 rounded-full bg-green-500" />

                    <span className="text-xs text-green-400">
                        ONLINE
                    </span>

                </div>

            </div>

        </div>
    );
}

export default LiveCamera;