function Topbar() {
    return (
        <header className="fixed left-64 right-0 top-0 z-10 h-20 border-b border-white/10 bg-[#0b0d10]/95 backdrop-blur">

            <div className="flex h-full items-center justify-between px-8">

                <div>
                    <p className="text-sm text-gray-400">
                        Security Operations
                    </p>

                    <h2 className="text-lg font-semibold text-white">
                        Command Center
                    </h2>
                </div>


                <div className="flex items-center gap-6">

                    {/* System status */}
                    <div className="flex items-center gap-2">

                        <span className="h-2 w-2 rounded-full bg-green-500"></span>

                        <span className="text-xs text-gray-400">
                            System Operational
                        </span>

                    </div>


                    {/* User */}
                    <div className="flex items-center gap-3">

                        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-sm font-semibold">
                            A
                        </div>

                        <div>
                            <p className="text-sm text-white">
                                Administrator
                            </p>

                            <p className="text-[10px] text-gray-500">
                                AUTHORIZED OPERATOR
                            </p>
                        </div>

                    </div>

                </div>

            </div>

        </header>
    );
}

export default Topbar;