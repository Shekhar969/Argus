function StatCard({
    title,
    value,
    description,
}) {
    return (
        <div className="rounded-xl border border-white/10 bg-white/[0.03] p-5">

            <p className="text-xs uppercase tracking-wider text-gray-500">
                {title}
            </p>

            <p className="mt-3 text-3xl font-semibold text-white">
                {value}
            </p>

            <p className="mt-2 text-xs text-gray-500">
                {description}
            </p>

        </div>
    );
}

export default StatCard;