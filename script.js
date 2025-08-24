async function buildNetwork(username) {
    const data = await fetchJson(`${API_BASE}/network/${username}`);
    const nodes = new vis.DataSet();
    const edges = new vis.DataSet();

    function addNodeRecursive(user, parent=null) {
        if (!user || nodes.get(user.login)) return;

        nodes.add({
            id: user.login,
            label: user.login,
            shape: 'circularImage',
            image: user.avatar_url,
            size: parent ? 20 : 40
        });

        if (parent) edges.add({ from: parent, to: user.login });

        if (user.children) {
            user.children.forEach(child => addNodeRecursive(child, user.login));
        }
    }

    addNodeRecursive(data);

    const container = document.getElementById("network");
    const graphData = { nodes, edges };
    const options = { physics: { stabilization: true } };
    new vis.Network(container, graphData, options);
}
