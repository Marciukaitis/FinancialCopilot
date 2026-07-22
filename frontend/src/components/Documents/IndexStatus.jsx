// import PropTypes from "prop-types";
// import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
// import LayersOutlinedIcon from "@mui/icons-material/LayersOutlined";
// import Box from "@mui/material/Box";
// import Chip from "@mui/material/Chip";
// import Stack from "@mui/material/Stack";
// import Typography from "@mui/material/Typography";

// function IndexStatus({ status }) {
//   const hasDocs = (status?.documents_count || 0) > 0;

//   return (
//     <Box>
//       <Typography variant="subtitle2" sx={{ mb: 1.5, color: "text.secondary" }}>
//         Documentos indexados
//       </Typography>

//       <Stack spacing={1.25}>
//         <Stack
//           direction="row"
//           justifyContent="space-between"
//           alignItems="center"
//           sx={{
//             px: 1.5,
//             py: 1.25,
//             borderRadius: 2,
//             bgcolor: "background.default",
//             border: "1px solid",
//             borderColor: "divider",
//           }}
//         >
//           <Stack direction="row" spacing={1} alignItems="center">
//             <DescriptionOutlinedIcon fontSize="small" color="action" />
//             <Typography variant="body2">PDFs</Typography>
//           </Stack>
//           <Typography variant="subtitle1" fontWeight={600}>
//             {status?.documents_count ?? 0}
//           </Typography>
//         </Stack>

//         <Stack
//           direction="row"
//           justifyContent="space-between"
//           alignItems="center"
//           sx={{
//             px: 1.5,
//             py: 1.25,
//             borderRadius: 2,
//             bgcolor: "background.default",
//             border: "1px solid",
//             borderColor: "divider",
//           }}
//         >
//           <Stack direction="row" spacing={1} alignItems="center">
//             <LayersOutlinedIcon fontSize="small" color="action" />
//             <Typography variant="body2">Chunks</Typography>
//           </Stack>
//           <Typography variant="subtitle1" fontWeight={600}>
//             {status?.chunks_indexed ?? 0}
//           </Typography>
//         </Stack>

//         <Chip
//           size="small"
//           label={hasDocs ? "Listo para consultar" : "Sin documentos"}
//           color={hasDocs ? "success" : "default"}
//           variant={hasDocs ? "filled" : "outlined"}
//           sx={{ alignSelf: "flex-start" }}
//         />
//       </Stack>
//     </Box>
//   );
// }

// IndexStatus.propTypes = {
//   status: PropTypes.shape({
//     documents_count: PropTypes.number,
//     chunks_indexed: PropTypes.number,
//     collection_name: PropTypes.string,
//   }),
// };

// IndexStatus.defaultProps = {
//   status: {
//     documents_count: 0,
//     chunks_indexed: 0,
//   },
// };

// export default IndexStatus;
